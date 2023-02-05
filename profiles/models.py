from django.db import models
from django.contrib.auth.models import User
from hoctap_main.models import post as Post

class profile(models.Model):
    username = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    about = models.TextField(default='người dùng không chia sẻ thông tin')
    roles = [
        ('S', 'Học sinh'),
        ('T', 'Giáo viên'),
        ('A', 'admin')
    ]
    ranks = [
        ('A', 'Vàng'),
        ('B', 'Bạc'),
        ('C', 'Đồng'),
        ('U', 'Chưa xếp hạng'),
    ]
    role = models.CharField(max_length=1 ,choices=roles, default='S')
    rank = models.CharField(max_length=1 ,choices=ranks, default='U')
    NumberOfPosts = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

class notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(blank=True, max_length=255)
    content = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)