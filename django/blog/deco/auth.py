import config
import functools
import requests
from django.shortcuts import render, redirect
from django_redis import get_redis_connection
redis_conn = get_redis_connection()


def check_login(func):
    '''
    用于检查登录状态的装饰器
    :param func: nactive func
    :return: func type
    '''

    wrapped = func

    @functools.wraps(wrapped)
    def wrapper(request, *args, **kwargs):
        session_id = request.COOKIES.get(config.session_sign)

        return_url = config.local_domain + request.get_full_path()
        if not session_id:
            return render(request, "center.html")
            return redirect("http://{login_url}?return={return_url}"
                            .format(login_url=config.login_url, return_url=return_url))
        elif redis_conn.get(session_id):
            # 设置cookie并更新expires
            rep = func(request, *args, **kwargs)
            rep.set_cookie("session_id", session_id, config.session_cookie_expires)
            # 更新cache expires
            redis_conn.set(config.session_sign, session_id)
            return rep
        else:
            data = {"token": config.ACCESS_TOKEN, 'client_sessionid': session_id}
            request_url = "http://" + config.AUTH_API
            rq = requests.post(request_url, json=data)
            if rq.status_code == 200:
                pass
            # request({session_id, token})
            # return_data = {'auth_status'}
            # if auth_status = True:
            #   redis_set(cookie_id) and cookie.set_cookie(sesseio, expires)
            # else:
            # return redirect(url)
            pass

        return redirect("http://{login_url}?return={return_url}"
                        .format(login_url=config.login_url, return_url=return_url))
    return wrapper
