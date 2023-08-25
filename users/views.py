from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages

from qnaboard.models import Post
from users.forms import LoginForm, SignupForm, MypageForm, CustomPasswordChangeForm
from users.models import User, RecycleLog


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
    return HttpResponseRedirect(request.GET.get("next") or "/")


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


def mypage_view(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if request.user.is_authenticated:
        ###############################################################################
        user = request.user
        user_name = User.objects.get(id=request.user.id)
        ###############################################################################
        if RecycleLog.objects.filter(user=user) != None:
            logs_num_list52 = []
            for i in range(52):
                logs_num_list52.append(
                    len(
                        list(RecycleLog.objects.filter(user=user, classify_item=str(i)))
                    )
                )
            total_logs_num = RecycleLog.objects.filter(user=user).count()
            null_logs_num = total_logs_num - sum(logs_num_list52)
            print(total_logs_num, logs_num_list52, null_logs_num)

            logs_num_list13 = []
            for i in range(13):
                logs_num_list13.append(sum(logs_num_list52[4 * i : 4 * (i + 1)]))
        ###############################################################################
        if request.method == "POST":
            form = MypageForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect("users:mypage_view")
        else:
            form = MypageForm(instance=user)
        context = {
            "form": form,
            "user": user,
            "user_name": user_name.username,
            "logs_num_list13": logs_num_list13,
            "total_logs_num": total_logs_num,
        }
        return render(request, "users/mypage.html", context)


def change_password_view(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if request.user.is_authenticated:
        user = request.user

        if request.method == "POST":
            form = CustomPasswordChangeForm(user, request.POST)
            if form.is_valid():
                user_auth = form.save()
                update_session_auth_hash(request, user_auth)  # Important!
                return redirect("users:mypage_view")
        else:
            form = CustomPasswordChangeForm(user)
        context = {"form": form, "user": user}
        return render(request, "users/change_password.html", context)
