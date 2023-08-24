from django.shortcuts import render
from .models import Notice


# notice 게시글 목록 조회
def nb_list(request):
    notices = Notice.objects.all().order_by("-nb_date")
    context = {"notices": notices}
    return render(request, "noticeboard/notice_list.html", context)


# notice 게시글 상세 조회
def nb_read(request, notice_id):
    notice = Notice.objects.get(id=notice_id)
    context = {"notice": notice}
    return render(request, "noticeboard/notice_read.html", context)
