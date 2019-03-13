from django.conf.urls import url
from center import views

urlpatterns = [
    url("", views.center),
]