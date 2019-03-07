from django.conf.urls import url
from account.views import RegisterView, RegisterApiView
from account import views as account_views


urlpatterns = [
    url(r'^reg/', RegisterView.as_view()),
    url(r'^api/reg/$', RegisterApiView.as_view()),
    url(r'^api/genVerifyImage/$', account_views.GenVerifyImage.as_view()),
]