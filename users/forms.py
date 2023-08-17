from django import forms


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
