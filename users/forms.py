from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from users.models import User


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "이메일 (형식에 맞게 기입)"},
        ),
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호 (4자리 이상)"},
        ),
    )


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"입력한 사용자명({username})은 이미 사용 중입니다")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"입력한 이메일({email})은 이미 사용 중입니다")
        return email

    def clean(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            self.add_error("password2", "비밀번호가 서로 불일치 합니다")

    def save(self):
        username = self.cleaned_data["username"]
        password1 = self.cleaned_data["password1"]
        email = self.cleaned_data["email"]

        user = User.objects.create_user(
            username=username, password=password1, email=email
        )
        return user


class MypageForm(UserChangeForm):
    password = None

    username = forms.CharField(
        label="닉네임",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "minlength": "2",
            }
        ),
    )
    email = forms.EmailField(
        label="이메일",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User()
        fields = ["username", "email"]


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="기존 비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control pass_form-control",
                "placeholder": "기존 비밀번호",
            },
        ),
    )
    new_password1 = forms.CharField(
        label="새 비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control pass_form-control",
                "placeholder": "새 비밀번호",
            },
        ),
    )
    new_password2 = forms.CharField(
        label="새 비밀번호 재확인",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control pass_form-control",
                "placeholder": "새 비밀번호 재확인",
            },
        ),
    )

    def clean(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")

        if old_password == new_password1:
            self.add_error(
                "old_password",
                forms.ValidationError("기존 비밀번호와 새 비밀번호가 서로 달라야 합니다"),
            )
        else:
            return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError("기존 비밀번호가 올바르지 않습니다. 다시 입력해 주세요.")
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("두 개의 새 비밀번호가 일치하지 않습니다.")
        return password2

    class Meta:
        model = get_user_model()
        fields = ["old_password", "new_password1", "new_password2"]
