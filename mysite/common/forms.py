from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    # UserCreationForm 에다 이메일을 추가하기위해 클래스 따로만들어 상속
    email=forms.EmailField(label="이메일")

    class Meta:
        model=User
        fields=("username", "password1", "password2", "email")