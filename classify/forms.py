from django import forms
from users.models import RecycleLog


class ClassifyForm(forms.ModelForm):
    widget = forms.FileInput(attrs={"class": "upload_form"})

    class Meta:  # 장고 모델 폼은 반드시 내부에 Meta 클래스 가져야 함
        model = RecycleLog
        fields = [
            "input_img",
        ]
        labels = {
            "input_img": "이미지",
        }
