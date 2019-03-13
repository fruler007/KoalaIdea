from django.shortcuts import render, redirect

# Create your views here.


def center(request):
    if request.method == 'GET':
        session_id = request.COOKIES.get("session_id")
        if not session_id:
            return redirect("http://127.0.0.1:8000/v1/login?return=127.0.0.1:8001/i")
        return render(request, 'center.html')