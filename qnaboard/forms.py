from django import forms
from qnaboard.models import Post, Comment


# 게시글 작성 폼
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["qb_title", "qb_content", "qb_image"]

        labels = {
            "qb_title": "제목",
            "qb_content": "내용",
            "qb_image": "첨부파일",
        }

        widgets = {
            "qb_title": forms.TextInput(
                attrs={
                    "class": "form-control w-50",
                    "placeholder": "질문 사항이나 인증내용의 제목을 입력해 주세요",
                    "style": "margin-bottom : 10px;",
                }
            ),
            "qb_content": forms.Textarea(
                attrs={
                    "class": "form-control w-75",
                    "placeholder": "자세한 질문 사항이나 인증 내용을 입력해주세요",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # 사용자 정보를 받기 위한 변수
        super().__init__(*args, **kwargs)
        # 이미지 업로드
        self.fields["qb_image"].required = False  # 필수 필드가 아님을 나타냄
        self.fields["qb_image"].widget.attrs.update(
            {
                "class": "form-control w-75",
                "placeholder": "첨부파일",
            }
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # 로그인한 사용자 정보 설정
        if commit:
            instance.save()
        return instance


# 댓글 작성 폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["qc_content"]

        # labels = {
        #     "qc_content": "댓글",
        # }

        widgets = {
            "qc_content": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "댓글 작성",
                    "style": "margin-bottom : 10px;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # 사용자 정보를 받기 위한 변수
        self.post = kwargs.pop("post", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # 로그인한 사용자 정보 설정
        if commit:
            instance.save()
        return instance


# 검색 기능
class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100)
