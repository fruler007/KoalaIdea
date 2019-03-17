from django.conf.urls import url
from authuser.views import access_cookie

urlpatterns = [
    url(r'^access_auth/$', access_cookie)
]