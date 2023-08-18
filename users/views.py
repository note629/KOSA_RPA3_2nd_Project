from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
from users.models import User


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
        context = {"form": form, "page_title": "Login"}
        return render(request, "users/login.html", context)
    else:
        form = LoginForm()
        context = {"form": form, "page_title": "Login"}
        return render(request, "users/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user, backend=backend)
            return redirect("/")

    else:
        form = SignupForm()

    context = {"form": form}
    return render(request, "users/signup.html", context)
