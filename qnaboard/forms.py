from django import forms
from qnaboard.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ["p_title", "user", "p_content"]
        fields = ["qb_title", "qb_content"]

        # labels = {
        #     "p_title": "제목",
        #     "user": "작성자",
        #     "p_content": "내용",
        # }
        labels = {
            "qb_title": "제목",
            "qb_content": "내용",
        }

        # 박스
        widgets = {
            "qb_title": forms.TextInput(
                attrs={
                    "class": "form-control w-50",  ## CSS
                    "placeholder": "질문 사항이나 인증내용의 제목을 입력해 주세요",  ## 힌트
                }
            ),
            # "user": forms.TextInput(
            #     attrs={"class": "form-control w-25", "placeholder": "작성자"}
            # ),
            "qb_content": forms.Textarea(
                attrs={
                    "class": "form-control w-75",
                    "placeholder": "자세한 질문 사항이나 인증 내용을 입력해주세요",
                }
            ),
        }
