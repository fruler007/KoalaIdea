from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile
from django.core.cache import cache
from utils.captcha.captcha import create_verify
import config
from django_redis import get_redis_connection
conn = get_redis_connection()
import re
from ret_code import RET
# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        pass


class RegisterApiView(View):
    def post(self, request):
        pass


# 生成验证图片
class GenVerifyImage(View):
    # @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        phone = request.GET.get("phone", "")
        ups = UserProfile.objects.filter(mobile=phone)
        # 检查手机号的合法性
        rm = re.match(r"^1\d{10}$", phone)
        if  not rm:
            return HttpResponse("请输入正确的手机号码")
        if ups.exists():
            return HttpResponse("该号码已经注册")

        # 判断redis列表长度
        verify_list_key = "img_verify_code_" + phone.lower()
        print(verify_list_key)
        conn.lrange(verify_list_key, 0, -1)
        llen = conn.llen(verify_list_key)
        if llen >= config.img_verify_list_length :
            return HttpResponse("请多少秒"
                                + str(config.img_verify_list_exprires)
                                + "再试")
        else:
            img_verify_code, img_bin = create_verify()
            conn.rpush(verify_list_key, img_verify_code)
            if llen == 0:
                conn.expire(verify_list_key, config.img_verify_list_exprires)
        return HttpResponse(img_bin, content_type="image/jpg")

    # @csrf_exempt
    def post(self, request):
        with open("1.jpg", mode='rb') as f:
            img = f.read()
        return HttpResponse(img, content_type="image/jpg")


# 响应短信验证码
class SmsVerifyCode(View):
    def get(self, request):
        phone = request.GET.get("phone", '')
        img_verify_code = request.GET.get("imgVerifyCode", '')
        if not re.match(r"^1\d{10}$", phone) \
                or len(img_verify_code) != config.img_verify_code_length:
            return HttpResponse(RET.INVALID_DATA)
        last_verify_code = conn.lindex("img_verify_code_" + phone, -1)
        if last_verify_code is None:
            return HttpResponse(RET.INVALID_DATA)
        else:
            last_verify_code = last_verify_code.decode()
            A = last_verify_code

        if last_verify_code.upper() == img_verify_code.upper():
            return HttpResponse(RET.SUCCESS, content_type="application/json")
        else:
            return HttpResponse(RET.INVALID_DATA, content_type="application/json")

