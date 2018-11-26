from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from forms import LoginForm


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