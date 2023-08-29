from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from requests import post

from .forms import NoticeForm
from .models import Notice


# notice 게시글 목록 조회
def nb_list(request):
    notices = Notice.objects.all().order_by("-nb_date")

    # 페이징 처리
    paginator = Paginator(notices, 7)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    context = {
        "notices": page_obj,
        "page_title": "공지사항 목록",
    }

    return render(request, "noticeboard/notice_list.html", context)


# notice 게시글 상세 조회
def nb_read(request, notice_id):
    notice = Notice.objects.get(id=notice_id)
    context = {
        "notice": notice,
        "page_title": "Title - " + notice.nb_title,
    }

    # 조회 수 증가
    notice.nb_view_count += 1
    notice.save()

    return render(request, "noticeboard/notice_read.html", context)


# notice 게시글 작성
def nb_create(request):
    if not request.user.is_authenticated:
        return redirect("noticeboard:notice_list")

    if request.user.is_authenticated:
        if request.method == "POST":
            notice_form = NoticeForm(request.POST, request.FILES, user=request.user)

            if notice_form.is_valid():
                print(request.FILES)
                notice = notice_form.save()
                return redirect("noticeboard:read", notice_id=notice.id)

        else:
            notice_form = NoticeForm()

        return render(
            request,
            "noticeboard/notice_create.html",
            {"notice_form": notice_form, "page_title": "공지사항 작성"},
        )


# notice 게시글 수정
def nb_update(request, notice_id):
    notice = Notice.objects.get(id=notice_id)

    if request.method == "POST":
        notice_form = NoticeForm(request.POST, request.FILES, instance=notice)

        if notice_form.is_valid():
            # if notice.nb_image and "nb_image":  # 이미지 제거
            # notice.nb_image.delete()
            print(request.FILES)
            notice_form.save()
            return redirect("noticeboard:read", notice_id=notice.id)

    else:
        notice_form = NoticeForm(instance=notice)

    return render(
        request,
        "noticeboard/notice_update.html",
        {"updateForm": notice_form, "page_title": "공지사항 수정"},
    )


# notice 게시글 삭제
def nb_delete(request, notice_id):
    notice = Notice.objects.get(id=notice_id)

    if not request.user.is_superuser:  # 슈퍼유저가 아니면 권한 없음 오류 발생
        raise PermissionDenied

    notice.delete()
    return redirect("noticeboard:list")
