from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        pass


class RegisterApiView(View):
    def post(self, request):
        pass


#生成验证图片
class GenVerifyImage(View):
    def get(self, request):
        with open("1551967549.jpg", mode='rb') as f:
            img = f.read()
        return HttpResponse(img, content_type="image/jpg")

