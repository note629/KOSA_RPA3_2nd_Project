from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 4:
            raise ValidationError("비밀번호가 너무 짧습니다.")

    def get_help_text(self):
        return "어드민 페이지에서 비밀번호 설정"
