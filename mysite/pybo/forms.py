from django import forms
from pybo.models import Question,Answer, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']
        """
        # form.as_p 를 사용안할경우 수작업 할거라 필요 x
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }"""
        labels={
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields=['content']
        labels={
            'content': '답변 내용'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']
        lanels={
            'content': '댓글 내용',
        }