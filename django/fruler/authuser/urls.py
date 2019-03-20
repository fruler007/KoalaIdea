from django.conf.urls import url
from authuser.views import set_cookie, test, test2

urlpatterns = [
    url(r'^access_auth/$', set_cookie),
    url(r'^test/$', test),
    url(r'^test2/$', test2)
]