# ModelForm
from django import forms

## 注册
class UserProfileForm(forms.Form):
    username = forms.CharFiled(max_length=128)
    password = forms.CharField(max_length=128)
    email = forms.EmailField(max_length=128)
    mobile = forms.CharField(max_length=64)
    reg_data=forms.DateTimeField()

