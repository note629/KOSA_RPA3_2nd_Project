from django import forms
from django.core.exceptions import ValidationError

from users.models import RecycleLog


class ClassifyForm(forms.ModelForm):
    class Meta:  # 장고 모델 폼은 반드시 내부에 Meta 클래스 가져야 함
        model = RecycleLog
        fields = [
            "input_img",
        ]
        labels = {
            "input_img": "이미지",
        }
