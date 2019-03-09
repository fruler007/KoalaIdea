from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile
from django.core.cache import cache
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
    # @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        phone = request.GET.get("phone")
        up = UserProfile.objeccts.get(mobile=phone);
        if(up):
            return HttpResponse("")

        with open("1.jpg", mode='rb') as f:
            img = f.read()
        return HttpResponse(img, content_type="image/jpg")

    # @csrf_exempt
    def post(self, request):
        with open("1.jpg", mode='rb') as f:
            img = f.read()
        return HttpResponse(img, content_type="image/jpg")