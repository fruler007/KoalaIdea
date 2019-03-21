from django.conf.urls import url
from account.views import RegisterView, RegisterApiView, LoginView
from account import views as account_views


urlpatterns = [
    url(r'^reg/', RegisterView.as_view()),
    url(r'login/', LoginView.as_view()),
    url(r'^api/reg/$', RegisterApiView.as_view()),
    url(r'^api/genVerifyImage/$', account_views.GenVerifyImage.as_view()),
    url(r'^api/smsVerifyCode/$', account_views.SmsVerifyCode.as_view()),
    url(r'^api/crossdomain/$', account_views.LoginSetCookieView.as_view()),
    url(r'^api/checklogin$', account_views.CheckLoginView.as_view()),

]