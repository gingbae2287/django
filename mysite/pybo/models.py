from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    subject=models.CharField(max_length=200)
    content=models.TextField()
    create_date=models.DateTimeField()
    modify_date=models.DateTimeField(null=True, blank=True) #blank=True는 form.is_balid 검사시 값이 없어도 됨

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    # on_delete 질문이 사라지면 해당 답변도 사라짐
    content=models.TextField()
    create_date=models.DateTimeField()
    modify_date=models.DateTimeField(null=True, blank=True)


class Comment(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    create_date=models.DateTimeField()
    modify_date=models.DateTimeField(null=True,blank=True)
    question=models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer=models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)