from django.db import models


# 게시글
class Post(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    qb_title = models.CharField(verbose_name="제목", max_length=30)
    qb_content = models.TextField("내용")
    qb_date = models.DateTimeField("작성일", auto_now_add=True)
    qb_view_count = models.IntegerField(verbose_name="조회수", default=0)

    def __str__(self):
        return self.qb_title


# 댓글
class Comment(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    qc_content = models.TextField("내용")
    qc_date = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return self.qc_content
