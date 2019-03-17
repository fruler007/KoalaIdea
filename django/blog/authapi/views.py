from django.shortcuts import render, HttpResponse

# Create your views here.


def cross_domain(request):
    if request.method == 'GET':
        session_id = request.GET.get("session_id", '1111')
        hp = HttpResponse("get session_Id")
        hp.set_cookie("session_id", session_id)
        return hp
    elif request.method == 'POST':
        pass