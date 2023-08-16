from django.db import models


# 게시글
class Post(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    p_title = models.CharField(max_length=30)
    p_content = models.TextField("내용")
    p_date = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return self.p_title


# 댓글
class Comment(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    c_content = models.TextField("내용")
    c_date = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return self.c_content
