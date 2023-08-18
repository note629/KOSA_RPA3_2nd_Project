from django.core.exceptions import PermissionDenied

from django.shortcuts import render, redirect

from qnaboard.forms import PostForm
from qnaboard.models import Post


# QnA 게시글 목록 조회
def qb_list(request):
    posts = Post.objects.all().order_by("-qb_date")
    context = {"posts": posts}
    return render(request, "qnaboard/qna_list.html", context)


# QnA 게시글 상세 조회
def qb_read(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {"post": post}
    return render(request, "qnaboard/qna_read.html", context)


# QnA 게시글 작성
def qb_create(request):
    if not request.user.is_authenticated:
        return redirect("qnaboard:list")

    if request.user.is_authenticated:
        if request.method == "POST":
            post_form = PostForm(request.POST, user=request.user)

            if post_form.is_valid():
                post_form.save()
                return redirect("qnaboard:list")

        else:
            post_form = PostForm(user=request.user)

        return render(request, "qnaboard/qna_create.html", {"post_form": post_form})


# QnA 게시글 수정
def qb_update(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post, user=request.user)

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
