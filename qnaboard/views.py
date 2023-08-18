from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests import post

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
    if request.method == "POST":
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.save()
            return redirect("qnaboard:list")

    else:
        post_form = PostForm()

    return render(request, "qnaboard/qna_create.html", {"post_form": post_form})


# QnA 게시글 수정
def qb_update(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        post.qb_title = request.POST["qb_title"]
        post.qb_content = request.POST["qb_content"]

        post.save()
        # return redirect("qnaboard:list")  # 리스트 페이지로 이동
        return redirect("qnaboard:read", post_id=post.id)  # 수정된 게시물의 상세 페이지로 이동

    else:
        updateForm = PostForm(instance=post)
        return render(request, "qnaboard/qna_update.html", {"updateForm": updateForm})


# QnA 게시글 삭제
def qb_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("qnaboard:list")


#     except Post.DoesNotExist:
#         return HttpResponse("해당 게시물을 찾을 수 없습니다.")
