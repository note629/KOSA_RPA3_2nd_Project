from django.shortcuts import render, redirect

from qnaboard.forms import PostForm
from qnaboard.models import Post


# 게시글 목록 조회
def p_list(request):
    posts = Post.objects.all().order_by("-id")
    context = {"posts": posts}
    return render(request, "qnaboard/qna_list.html", context)


# 게시글 작성
def p_create(request):
    if request.method == "POST":
        # 입력된 데이터를 데이터베이스에 저장!

        ## 사용자가 입력한 내용을 가지고 ModelForm객체를 생성
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.save()
            return redirect("qnaboard:list")

    else:
        # 사용자 입력양식을 사용자에게 보여줌
        ## 데이터가 없는 ModelForm객체를 생성
        post_form = PostForm()

    return render(request, "qnaboard/qna_create.html", {"post_form": post_form})
