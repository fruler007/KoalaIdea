from django.conf.urls import url
from authuser.views import set_cookie, test

urlpatterns = [
    url(r'^access_auth/$', set_cookie),
    url(r'^test/$', test),
]