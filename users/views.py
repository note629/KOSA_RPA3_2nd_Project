from django.shortcuts import render


# login_view 구현
def login_view(request):
    return render(request, "users/login.html")
