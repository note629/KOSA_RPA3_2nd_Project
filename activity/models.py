from django.db import models

from users.models import User, RecycleLog


class GalleryLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recyclelog = models.ForeignKey(
        RecycleLog, on_delete=models.CASCADE, related_name="gallerylogs", unique=True
    )
    #
    # def __str__(self):
    #     return self.user_id


class GalleryLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gallerylog = models.ForeignKey(GalleryLog, on_delete=models.CASCADE)
    #
    # def __str__(self):
    #     return self.user_id
