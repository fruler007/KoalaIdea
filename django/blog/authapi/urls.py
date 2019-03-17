from django.conf.urls import url
from authapi import views

urlpatterns = [
    url(r'^crossdomain/', views.cross_domain),
]