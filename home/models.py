from django.db import models
from django.contrib.auth.models import User

class faq(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    def __str__(self):
        return self.title

AdminRoles = [
    ('A', 'quản lí'), #HA = Head Admin
    ('B', 'kiểm duyệt viên'), #KD = Kiểm Duyệt
    ('C', 'giúp đỡ'), # HP = Hepler
]

class AdminUser(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=AdminRoles, max_length=2, help_text='vai trò của người quản lí')
    description = models.TextField(help_text='mô tả | bạn lưu ý phải xóa hết text trong field rồi ghi mô tả của bạn nhé', default='không có mô tả về admin này!')
    avatar = models.ImageField(upload_to='images', null=False, default='images/default.png', help_text='Lưu ý khi upload file ảnh: ảnh tỉ lệ 1:1 (hình vuông) và phải để tên file là họ và tên của bạn + năm sinh | ví dụ: nguyenminhhieu08')

    def __str__(self):
        return f"{self.username}, {self.role}"

class announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.title} {self.author} {self.date}"

class BadWord(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.word}"