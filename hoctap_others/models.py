from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    detail = models.CharField(max_length=255, default="")
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.title}"

class news(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.title} {self.date}"