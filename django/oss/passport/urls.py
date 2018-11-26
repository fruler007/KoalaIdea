#
from django.conf.urls import url
from sso.passport import views


urlpatterns = [
    url(r'^login/$', views.login)
]