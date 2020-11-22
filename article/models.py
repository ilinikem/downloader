from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Download(models.Model):
    id = models.AutoField(primary_key=True)
    jsonData = models.JSONField()
    created_at = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        # выводим текст поста
        return self.jsonData