from django import forms

from noticeboard.models import Notice
from qnaboard.models import Post, Comment


# notice 작성 폼
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ["nb_title", "nb_content", "nb_image"]

        labels = {
            "nb_title": "제목",
            "nb_content": "내용",
            "nb_image": "첨부파일",
        }

        widgets = {
            "nb_title": forms.TextInput(
                attrs={
                    "class": "form-control w-50",
                    "placeholder": "공지 제목",
                    "style": "margin-bottom : 10px;",
                }
            ),
            "nb_content": forms.Textarea(
                attrs={
                    "class": "form-control w-75",
                    "placeholder": "공지 내용 작성",
                }
            ),
        }

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop("user", None)  # 사용자 정보를 받기 위한 변수
    #     super().__init__(*args, **kwargs)
    #     # 이미지 업로드
    #     self.fields["nb_image"].widget.attrs.update(
    #         {
    #             "class": "form-control w-75",
    #             "placeholder": "첨부파일",
    #         }
    #     )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # 이미지 업로드
        self.fields["nb_image"].required = False  # 필수 필드가 아님을 나타냄
        self.fields["nb_image"].widget.attrs.update(
            {
                "class": "form-control w-75",
                "placeholder": "첨부파일",
            }
        )
