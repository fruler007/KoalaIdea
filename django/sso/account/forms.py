# ModelForm
from django import forms
from django.forms import fields
import config


## 注册
class UserProfileForm(forms.Form):
    username_rex = '^[A-Za-z][A-Za-z0-9_]{%s,%s}$' \
                   % (config.reg_username_min_len, config.reg_username_max_len)
    password_rex = '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\!]).{8,32}$'

    email = forms.EmailField(max_length=128, required=False)
    phone = fields.RegexField("^1\d{10}$",
                              required=True,
                              error_messages={
                                  'invalid': "手机号格式不对",
                                  'required': '手机号不能为空'
                              })

    username = fields.RegexField(username_rex,
                                 required=True,
                                 error_messages={
                                     'invalid': '用户名格式不合法',
                                     'required': '用户名不能为空'
                                 })

    password = fields.RegexField(password_rex,
                                 required=True,
                                 error_messages={
                                     'invalid': '密码不合法',
                                     'required': '密码不能为空'
                                 })

    password2 = fields.RegexField(password_rex,
                                 required=True,
                                 error_messages={
                                     'invalid': '密码不合法',
                                     'required': '密码不能为空'
                                 })


