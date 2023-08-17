from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm


# login_view 구현
def login_view(request):
    if request.method == "POST":
        # LoginForm 인스턴스 생성, 입력 데이터는 request.POST 사용
        form = LoginForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            print(user)
            if user:
                login(request, user)
                print("성공")
                return redirect("/")
            else:
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다")

        # 생성한 LoginForm 인스턴스를 template에 "form"이라는 키로 전달 함
        context = {"form": form}
        return render(request, "users/login.html", context)
    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)
