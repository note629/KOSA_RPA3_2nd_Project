from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404

from qnaboard.forms import PostForm, CommentForm, SearchForm
from qnaboard.models import Post, Comment

from django.db.models import Q


# QnA 게시글 목록 조회
def qb_list(request):
    posts = Post.objects.all().order_by("-qb_date")

    # 검색 기능
    search_form = SearchForm(request.GET)
    query = request.GET.get("query")

    if query:
        posts = Post.objects.filter(
            Q(qb_title__icontains=query) | Q(qb_content__icontains=query)
        ).order_by("-qb_date")
    else:
        posts = Post.objects.all().order_by("-qb_date")

    # 페이징 처리
    paginator = Paginator(posts, 5)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    context = {
        "posts": page_obj,
        "search_form": search_form,
        "query": query,
        "page_title": "QnA 목록",
    }

    return render(request, "qnaboard/qna_list.html", context)


def qb_read(request, post_id):
    try:
        post = Post.objects.get(id=post_id)

    except Post.DoesNotExist:
        return HttpResponse("해당 게시물을 찾을 수 없습니다.")

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "page_title": "Title - " + post.qb_title,
    }

    # 조회 수 증가
    post.qb_view_count += 1
    post.save()

    # 댓글 기능
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
                post = post_form.save()
                return redirect("qnaboard:read", post_id=post.id)

        else:
            post_form = PostForm()

        return render(
            request,
            "qnaboard/qna_create.html",
            {"post_form": post_form, "page_title": "QnA 작성"},
        )


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

    return render(
        request,
        "qnaboard/qna_update.html",
        {"updateForm": post_form, "page_title": "QnA 수정"},
    )


# QnA 게시글 삭제
def qb_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.user:  # 작성자만 삭제 가능
        raise PermissionDenied  # 권한 없음

    post.delete()
    return redirect("qnaboard:list")


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
