from django.conf.urls import url
from account.views import RegisterView, RegisterApiView


urlpatterns = [
    url(r'^reg/', RegisterView.as_view()),
    url(r'^api/reg/$', RegisterApiView.as_views()),
]