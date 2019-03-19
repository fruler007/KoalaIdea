import config
import datetime
import json
import requests
from django.shortcuts import render, HttpResponse, redirect
from django_redis import get_redis_connection
redis_conn = get_redis_connection()


# Create your views here.
def set_cookie(request):
    if request.method == 'GET':
        callback = request.GET.get("jsoncallback")
        session_id = request.GET.get("session_id", "")
        KLID = request.GET.get("KLID", "")
        return_callback = "TestJson2" + '(["A", "b", "c"], "bbb")'
        rp = HttpResponse(return_callback)
        expires_date = datetime.datetime.now() + datetime.timedelta(
            days=config.session_cookie_expires/86400)

        if all((session_id, KLID)):
            domain = request.environ.get('HTTP_HOST')
            # redis_conn.set("fruler_session_id", session_id)
            # redis_conn.expire("fruler_session_id", config.session_redis_expires/86400)
            # redis_conn.set("fruler_KLID", KLID)
            # redis_conn.expire("fruler_KLID", config.session_redis_expires/86400)
            rp.set_cookie("session_id", session_id, path='/', expires=expires_date, domain=domain)
            rp.set_cookie("KLID", KLID, path='/', expires=expires_date, domain=domain)
        return rp

    elif request.method == 'POST':
        return HttpResponse("auth user POST ")


def test(request):
    if request.method == 'GET':
        session_id = request.COOKIES.get("session_id", "")
        KLID = request.COOKIES.get("KLID", "")
        if all((session_id, KLID)):
            session_id_cache = redis_conn.get(session_id)
            klid_cache = redis_conn.get(KLID)

            session_id_cache = 0
            klid_cache = 0
            if all((session_id_cache, klid_cache)):
                return HttpResponse("login success")
            else:
                checklogin_data = {"session_id": session_id,
                                  'KLID': KLID,
                                  'token': config.checklogin_token}
                checklogin_response = requests.post('http://' + config.checklogin_url,
                                                    json=checklogin_data)
                return_data = json.loads(checklogin_response.content.decode("utf-8"))
                if return_data.get("code") == 202:
                    return HttpResponse("success")

        # 生成全路径url
        local_host = request.environ.get("HTTP_HOST")
        url = "http://" + config.login_url + "?return_url=" \
              + local_host + request.path
        params_list = []
        for k, v in request.GET.items():
            params_list.append(k + "=" + v)
        url += "?" + "&".join(params_list)

        return redirect(url)