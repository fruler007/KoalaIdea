from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'passport/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        return_url = request.GET.get('return_url', settings.default_return_url)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(return_url)
        else:
            error_login = "username or password error !"
            return render(request, 'passport/login.html',
                          {'error_login': error_login})
