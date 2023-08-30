from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class RecycleLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    use_date = models.DateTimeField(auto_now_add=True)
    input_img = models.ImageField(upload_to="recycle_img/")
    classify_item = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.classify_item
