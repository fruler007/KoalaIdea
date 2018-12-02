from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from forms import LoginForm
from utils.smtp import smtp_instance
from email.mime.text import MIMEText
from email.header import Header
from django.conf import settings
from django import forms
import logging
from response_code import RET
from django.core.exceptions import ValidationError
import random
import json
from django.core.cache import cache
import datetime


# Create your views here.
# 用户登录验证视图
def login(request):
    if request.method == 'GET':
        return render(request, 'passport/login.html')
    elif request.method == 'POST':
        # 验证用户名与密码格式是否合法
        form = LoginForm(request.POST)
        if not form.is_valid():
            error_login = "用户名或密码格式有误"
            return render(request, 'passport/login.html',
                          {'error_login': error_login})

        return_url = request.GET.get('return_url', settings.default_return_url)
        user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password"])
        if user:
            login(request, user)
            return redirect(return_url)
        else:
            error_login = "用户名或密码有误!"
            return render(request, 'passport/login.html',
                          {'error_login': error_login})


# 用户注册视图
def register(request):
    if request.method == "GET":
        return render(request, "passport/register.html")
    elif request.method == 'POST':
        return render(request, "passport/register.html")


# 获取验证码
def reg_mail_code(request):
    if request.method == "POST":
        f = forms.EmailField()
        email = request.POST.get("email")
        try:
            f.clean(email)
        except ValidationError as e:
            logging.error("is validation email address")
            return HttpResponse(json.dumps({"ret_code": RET.VALIDATION_DATA}),
                                content_type="application/json")

        # 查询注册邮箱在一定之间内多次提交
        key = email + "email_register"
        value = datetime.datetime.now()
        if cache.has_key(key):
            return HttpResponse(json.dumps({"ret_code": RET.FRE_REQUEST}),
                                content_type="application/json")
        cache.set(key, value, settings.EMAIL_REQUEST_INTERVAL)

        # 发送验证码
        random_code = random.randint(10**(settings.EMAIL_CODE_LENGTH-1),
                                     10**(settings.EMAIL_CODE_LENGTH)-1)
        body = "欢迎注册KoalaBuy:" \
               "\n    你的注册码为: {random_code}".format(random_code=random_code)
        message = MIMEText(body, 'plain', 'utf-8')
        message["subject"] = "Koalabuy邮件注册码"
        message["from"] = settings.EMAIL_HOST_USER
        message["to"] = email
        smtp_instance.sendmail(settings.EMAIL_HOST_USER,
                               [email,],
                               message.as_string())


        return HttpResponse(json.dumps({"RET_CODE": RET.ACCEPT}),
                            content_type='application/json')
