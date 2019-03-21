import config
import datetime
import json
import re
import uuid
from account.models import UserProfile
from account.forms import UserProfileForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django_redis import get_redis_connection

conn = get_redis_connection()
from hashlib import md5
from ret_code import RET
from lib.dysms_python.sms_send import send_sms
from utils.captcha.captcha import create_verify
from utils.tool import random_sms, hash_str
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        up_form = UserProfileForm(request.POST)
        if not up_form.is_valid():
            print(up_form.data)
            print(up_form.clean())
            return redirect("/")
        if up_form.data['password'] != up_form.data['password2']:
            return redirect("/")

        hash_password = hash_str(up_form.cleaned_data['password'], config.password_salt)
        up = UserProfile.objects.create(
            username=up_form.cleaned_data['username'],
            password=hash_password,
            phone=up_form.cleaned_data['phone'],
            )
        up.save()
        return redirect("/login")


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
        ups = UserProfile.objects.filter(phone=phone)
        # 检查手机号的合法性
        rm = re.match(r"^1\d{10}$", phone)
        if not rm:
            return HttpResponse("请输入正确的手机号码")
        if ups.exists():
            return HttpResponse("该号码已经注册")

        # 判断redis列表长度
        verify_list_key = "img_verify_code_" + phone.lower()
        print(verify_list_key)
        conn.lrange(verify_list_key, 0, -1)
        llen = conn.llen(verify_list_key)
        if llen >= config.img_verify_list_length:
            return HttpResponse("请多少秒"
                                + str(config.img_verify_list_expires)
                                + "再试")
        else:
            img_verify_code, img_bin = create_verify()
            conn.rpush(verify_list_key, img_verify_code)
            if llen == 0:
                conn.expire(verify_list_key, config.img_verify_list_expires)
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
        # 判断图片验证码是否存
        last_img_verify_code = conn.lindex("img_verify_code_" + phone, -1)
        if last_img_verify_code is None:
            return HttpResponse(RET.INVALID_DATA)
        else:
            last_img_verify_code = last_img_verify_code.decode()

        if last_img_verify_code.upper() != img_verify_code.upper():
            return HttpResponse(RET.INVALID_DATA, content_type="application/json")

        # 缓存短信
        sms_list_key = "sms_verify_" + phone
        sms_list_len = conn.llen(sms_list_key)
        # 频繁请求短信验证码处理方式
        if sms_list_len >= config.sms_verify_list_length:
            return HttpResponse(RET.FRE_REQ_ERROR, content_type="application/json")
        else:
            # 正在范围内短信验证码处理方式
            if sms_list_len == 0:
                random_sms_code = random_sms(config.sms_verify_length)
                send_sms(
                    business_id=uuid.uuid4().__str__(),
                    phone_numbers=phone,
                    sign_name=config.sms_sign,
                    template_code=config.template_code,
                    template_param="{'code':%s} " % random_sms_code
                )
                conn.rpush(sms_list_key, random_sms_code)
                conn.expire(sms_list_key, config.sms_verify_list_expires)
            else:
                random_sms_code = conn.lindex(sms_list_key, -1).decode()
                send_sms(business_id=uuid.uuid4().__str__(),
                         phone_numbers=phone,
                         sign_name=config.sms_sign,
                         template_code=config.template_code,
                         template_param="{'code':%s} " % random_sms_code
                         )
                conn.lpush(sms_list_key, "1")

            return HttpResponse(RET.SUCCESS, content_type="applicaiton/json")


# 登录页面
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        return_url = "http://" + request.GET.get('return_url', config.center_url)
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        req_host = request.environ.get("HTTP_HOST")

        try:
            up1 = UserProfile.objects.get(phone=phone)
        except ObjectDoesNotExist as e:
            data = {"code": 0, "msg": "username or password was wrong !"}
            return HttpResponse(json.dumps(data))
        p1 = up1.password
        p2 = hash_str(password, config.password_salt)
        if p1 != p2:
            data = {"code": 0, "msg": "username or password was wrong !"}
        else:
            hash_password = md5(password.encode()).hexdigest()
            session_id = md5(phone.encode("utf-8")).hexdigest()
            klid = md5((phone + config.cookie_salt).encode("utf-8")).hexdigest()
            klid_value = md5((klid+req_host).encode("utf-8")).hexdigest()
            user_info = {'username': 'dandan', 'phone': phone}
            conn.set(session_id, str(user_info))
            conn.expire(session_id, config.session_cache_expires)
            conn.set(klid, klid_value )
            conn.expire(klid, config.session_cache_expires)

            cookies = {"session_id": session_id,
                       'KLID': klid}
            data = {"cross_region": config.cross_domain,
                    "cookies": cookies,
                    "return_url": return_url,
                    'code': 1,
                    'msg': 'success'}

        return HttpResponse(json.dumps(data))


# 登录cookie设置接口
class LoginSetCookieView(View):
    def get(self, request):
        rp = HttpResponse()
        session_id = request.GET.get("session_id", "")
        klid = request.GET.get("KLID", "")
        expires_data = datetime.datetime.now() + datetime.timedelta(days=1)
        if all([session_id, klid]):
            rp.set_cookie("session_id", session_id, expires=expires_data,
                          domain=config.main_domain, path="/")
            rp.set_cookie("KLID", klid, expires=expires_data,
                          domain=config.main_domain, path="/")
        return rp

    def post(self, requiest):
        pass


# 检查登录状态
class CheckLoginView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super( CheckLoginView, self).dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request):
        # 验证口令
        json_data = json.loads(request.body.decode())
        token = json_data.get("token", "")
        if token != config.checklogin_token:
            return_data = dict.update(RET.AUTH_ERROR)
            return HttpResponse(json.dumps(return_data))

        # 查询登录状态
        req_data = json.loads(request.body.decode("utf-8"))
        session_id = req_data.get("session_id", "")
        klid = req_data.get('KLID', "")
        session_id_cache = conn.get(session_id)
        klid_cache = conn.get(klid)

        if all((session_id_cache, klid_cache)):
            conn.expire(session_id, config.session_cache_expires )
            conn.expire(klid, config.session_cache_expires )
            return_data = RET.HAVE_LOGIN
            return_data.update({"sesseion_id": session_id, 'KLID': klid})

        else:
            return_data = RET.NON_LOGIN
            print(return_data)
        return HttpResponse(json.dumps(return_data), content_type="application/json")


# 个人中心
class PersonCenterView(View):
    def get(self, request):
        return render(request, "personcenter.html")