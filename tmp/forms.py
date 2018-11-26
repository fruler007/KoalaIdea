from django import forms


class LoginForm(forms.Form):
    username = forms.EmailField(label="你的邮箱")
    password = forms.CharField(label="你的登录密码", min_length=8)