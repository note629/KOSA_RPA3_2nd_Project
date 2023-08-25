from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404

from qnaboard.forms import PostForm, CommentForm
from qnaboard.models import Post, Comment


# QnA 게시글 목록 조회
def qb_list(request):
    posts = Post.objects.all().order_by("-qb_date")
    context_posts = {"posts": posts}

    # 페이징 처리
    # paginator = Paginator(posts, 4)
    # page_num = int(request.GET.get("page", 1))
    # page = paginator.get_page(page_num)

    # context_page = {"page": page}

    return render(request, "qnaboard/qna_list.html", context_posts)


# QnA 게시글 상세 조회
# def qb_read(request, post_id):
#     post = Post.objects.get(id=post_id)
#     context = {"post": post}
#     return render(request, "qnaboard/qna_read.html", context)
##############
def qb_read(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse("해당 게시물을 찾을 수 없습니다.")

    comments = Comment.objects.filter(post=post)
    context = {"post": post, "comments": comments}

    if request.user.is_authenticated:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                return redirect("qnaboard:read", post_id=post.id)
        else:
            comment_form = CommentForm()

        context["comment_form"] = comment_form

    return render(request, "qnaboard/qna_read.html", context)


# QnA 게시글 작성
def qb_create(request):
    if not request.user.is_authenticated:
        return redirect("qnaboard:list")

    if request.user.is_authenticated:
        if request.method == "POST":
            post_form = PostForm(request.POST, request.FILES, user=request.user)

            if post_form.is_valid():
                post_form.save()
                return redirect("qnaboard:list")

        else:
            post_form = PostForm()

        return render(request, "qnaboard/qna_create.html", {"post_form": post_form})


# QnA 게시글 수정
def qb_update(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        post_form = PostForm(
            request.POST, request.FILES, instance=post, user=request.user
        )

        if post_form.is_valid():
            post_form.save()
            return redirect("qnaboard:read", post_id=post.id)

    else:
        post_form = PostForm(instance=post, user=request.user)

    return render(request, "qnaboard/qna_update.html", {"updateForm": post_form})


# QnA 게시글 삭제
def qb_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.user:  # 작성자만 삭제 가능
        raise PermissionDenied  # 권한 없음

    post.delete()
    return redirect("qnaboard:list")


#     except Post.DoesNotExist:
#         return HttpResponse("해당 게시물을 찾을 수 없습니다.")


def qbc_update(request, post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)

    if request.method == "POST":
        comment_content = request.POST.get("comment_content")
        comment.qc_content = comment_content
        comment.save()

    return redirect("qnaboard:read", post_id=post.id)


def qbc_delete(request, post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    if request.user != comment.user:
        raise PermissionDenied

    comment.delete()

    return redirect("qnaboard:read", post_id=post.id)
