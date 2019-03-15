import config
import requests
from django.shortcuts import render
from django_redis import get_redis_connection
from deco.auth import check_login
redis_conn = get_redis_connection()
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.
# @check_login
@xframe_options_exempt
def center(request):
    if request.method == 'GET':
        rd = render(request, "center.html")
        rd["Access-Control-Allow-Credentials"] = True
        rd["Access-Control-Allow-Origin"] = "http://account.koala.com"
        # rd["Access-Control-Allow-Methods"] = "GET,POST,PUT,POST"
        # rd["Access-Control-Allow-Headers"] = "x-requested-with,content-type"
        return rd
