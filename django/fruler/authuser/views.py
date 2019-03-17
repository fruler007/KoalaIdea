from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse


# Create your views here.
def access_cookie(request):
    if request.method == 'GET':
        callback = request.GET.get("jsoncallback")
        return_callback = "TestJson2" + '(["A", "b", "c"], "bbb")'
        print(type(callback))
        return HttpResponse(return_callback)
    elif request.method == 'POST':
        return HttpResponse("auth user POST ")