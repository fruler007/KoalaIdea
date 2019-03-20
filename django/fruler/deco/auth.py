import config
import json
import requests
from django.shortcuts import HttpResponse, redirect
from django_redis import get_redis_connection
redis_conn = get_redis_connection()


# 检查登录装饰器
def checklogin(func):
    def wrapped(request, *args, **kwargs):
        if request.method == 'GET':
            session_id = request.COOKIES.get("session_id", "")
            KLID = request.COOKIES.get("KLID", "")
            if all((session_id, KLID)):
                session_id_cache = redis_conn.get(session_id)
                klid_cache = redis_conn.get(KLID)

                session_id_cache = 0
                klid_cache = 0
                if all((session_id_cache, klid_cache)):
                    redis_conn.expire(session_id, config.session_redis_expires)
                    redis_conn.expire(KLID, config.session_redis_expires)
                    return func(request, *args, **kwargs)
                else:
                    checklogin_data = {"session_id": session_id,
                                       'KLID': KLID,
                                       'token': config.checklogin_token}
                    checklogin_response = requests.post(
                        'http://' + config.checklogin_url,
                        json=checklogin_data)
                    return_data = json.loads(
                        checklogin_response.content.decode("utf-8"))
                    if return_data.get("code") == 202:
                        return func(request, *args, **kwargs)

            # 生成全路径url
            local_host = request.environ.get("HTTP_HOST")
            url = "http://" + config.login_url + "?return_url=" \
                  + local_host + request.path
            params_list = []
            for k, v in request.GET.items():
                params_list.append(k + "=" + v)
            url += "?" + "&".join(params_list)

            return redirect(url)

    return wrapped