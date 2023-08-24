from django.db import models


# 공지
class Notice(models.Model):
    nb_title = models.CharField(verbose_name="공지 제목", max_length=50)
    nb_content = models.TextField(verbose_name="공지 내용")
    nb_date = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    nb_view_count = models.IntegerField(verbose_name="조회수", default=0)
    nb_image = models.ImageField(upload_to="noticeboard/", blank=True, null=True)

    def __str__(self):
        return self.nb_title


# 댓글 없음
