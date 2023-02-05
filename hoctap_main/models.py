from django.db import models
from django.contrib.auth.models import User

# Post 

class post(models.Model):
    post_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    NumberOfLike = models.PositiveIntegerField(default=0)
    NumberOfDislike = models.PositiveIntegerField(default=0)
    interactiveUsers = models.JSONField(blank=True, default=dict)

    is_verify = models.BooleanField(default=False)
    is_publish = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post_id}. Verified: {self.is_verify}, published: {self.is_publish}"

class QnA(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True)
    questioner = models.CharField(max_length=200)
    answerer = models.CharField(max_length=200)
    is_open_chat = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.post} - {self.is_finished}: {self.question}"

class chatQnA(models.Model):
    QnA = models.ForeignKey(QnA, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    isHide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.content}"

# Test 
class test(models.Model):
    test_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    NumberOfQuestions = models.PositiveIntegerField()
    correctAnswers = models.JSONField(default=dict)
    userJoined = models.JSONField(blank=True, default=dict)

    is_verify = models.BooleanField(default=False)
    is_publish = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_id}. Verified: {self.is_verify}, published: {self.is_publish}"

class QnAForTest(models.Model):
    test = models.ForeignKey(test, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True)
    questioner = models.CharField(max_length=200)
    answerer = models.CharField(max_length=200)
    is_open_chat = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.test} - {self.is_finished}: {self.question}"

class chatQnAForTest(models.Model):
    QnAForTest = models.ForeignKey(QnA, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    isHide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.content}"
