import math
import os
import shutil

from django.shortcuts import render, redirect
from ultralytics import YOLO

from classify.forms import ClassifyForm
from users.models import RecycleLog


ai_model = YOLO("static/model/best.pt")


def image_upload(request):
    if request.method == "POST":
        form = ClassifyForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.user_id = request.user.id
            log.save()
            return redirect("classify:classify_yolo")
    else:
        form = ClassifyForm()  # request.method 가 'GET'인 경우

    context = {
        # "results": results,이것
        "form": form
    }
    return render(request, "classify/classify.html", context)


def classify_yolo(request):
    classify_list = [
        "철캔_훼손 안 됨_오염안됨",
        "철캔_훼손 안 됨_이물질 있음",
        "철캔_훼손됨_이물질 없음",
        "철캔_훼손됨_이물질 있음",
        "알루미늄캔_훼손 안 됨_이물질 없음",
        "알루미늄캔_훼손 안 됨_이물질 있음",
        "알루미늄캔_훼손됨_이물질 없음",
        "알루미늄캔_훼손됨_이물질 있음",
        "종이_훼손 안 됨_이물질 없음",
        "종이_훼손 안 됨_이물질 있음",
        "종이_훼손됨_이물질 없음",
        "종이_훼손됨_이물질 있음",
        "패트병(무색)_훼손 안 됨_이물질 없음",
        "패트병(무색)_훼손 안 됨_이물질 있음",
        "패트병(무색)_훼손됨_이물질 없음",
        "패트병(무색)_훼손됨_이물질 있음",
        "패트병(유색)_훼손 안 됨_이물질 없음",
        "패트병(유색)_훼손 안 됨_이물질 있음",
        "패트병(유색)_훼손됨_이물질 없음",
        "패트병(유색)_훼손됨_이물질 있음",
        "플라스틱(PE)_훼손 안 됨_이물질 없음",
        "플라스틱(PE)_훼손 안 됨_이물질 있음",
        "플라스틱(PE)_훼손됨_이물질 없음",
        "플라스틱(PE)_훼손됨_이물질 있음",
        "플라스틱(PP)_훼손 안 됨_이물질 없음",
        "플라스틱(PP)_훼손 안 됨_이물질 있음",
        "플라스틱(PP)_훼손됨_이물질 없음",
        "플라스틱(PP)_훼손됨_이물질 있음",
        "플라스틱(PS)_훼손 안 됨_이물질 없음",
        "플라스틱(PS)_훼손 안 됨_이물질 있음",
        "플라스틱(PS)_훼손됨_이물질 없음",
        "플라스틱(PS)_훼손됨_이물질 있음",
        "스티로폼_훼손 안 됨_이물질 없음",
        "스티로폼_훼손 안 됨_이물질 있음",
        "스티로폼_훼손됨_이물질 없음",
        "스티로폼_훼손됨_이물질 있음",
        "비닐_훼손 안 됨_이물질 없음",
        "비닐_훼손 안 됨_이물질 있음",
        "비닐_훼손됨_이물질 없음",
        "비닐_훼손됨_이물질 있음",
        "유리(갈색)_훼손 안 됨_이물질 없음",
        "유리(갈색)_훼손 안 됨_이물질 있음",
        "유리(갈색)_훼손됨_이물질 없음",
        "유리(갈색)_훼손됨_이물질 있음",
        "유리(녹색)_훼손 안 됨_이물질 없음",
        "유리(녹색)_훼손 안 됨_이물질 있음",
        "유리(녹색)_훼손됨_이물질 없음",
        "유리(녹색)_훼손됨_이물질 있음",
        "유리(투명)_훼손 안 됨_이물질 없음",
        "유리(투명)_훼손 안 됨_이물질 있음",
        "유리(투명)_훼손됨_이물질 없음",
        "유리(투명)_훼손됨_이물질 있음",
    ]

    latest_log = (
        RecycleLog.objects.filter(user_id=request.user.id).order_by("-use_date").first()
    )  # /media/recycle_img/374745_01002_220728_P1_T1.jpg
    # print(latest_log.input_img.url)
    image_url = latest_log.input_img.url
    image_file = image_url.split("/")[-1]
    image_file_name = image_file.split(".")[0]
    print(image_file)
    print(image_file_name)
    if os.path.isfile("runs/detect/results/labels/" + image_file_name + ".txt"):
        os.remove("runs/detect/results/labels/" + image_file_name + ".txt")
    results = ai_model(
        image_url[1:],
        save_txt=True,
        save_conf=True,
        # conf=0.5,
        save=True,
        name="results",
        exist_ok=True,
    )

    from_file_path = "runs/detect/results/" + image_file  # 복사할 파일
    to_file_path = "media/classify_img/" + image_file  # 복사 위치 및 파일 이름 지정
    shutil.copy(from_file_path, to_file_path)

    txt_result = open("runs/detect/results/labels/" + image_file_name + ".txt", "r")
    # print(txt_result.readlines())
    result_list = [line for line in txt_result.readlines()]
    result_list_split_obj = (result_list[0].split(" "))[0]
    result_list_split_acc = (result_list[0].split(" "))[-1]

    result_obj = classify_list[int(result_list_split_obj)]
    result_obj_split_name = (result_obj.split("_"))[0]
    result_obj_split_dame = (result_obj.split("_"))[1]
    result_obj_split_dirt = (result_obj.split("_"))[2]
    results_acc = round(float(result_list_split_acc) * 100, 2)
    print(image_file)
    if float(result_list_split_acc) > 0.5:
        txt_result.close()
        context = {
            "result_obj_split_name": result_obj_split_name,
            "result_obj_split_dame": result_obj_split_dame,
            "result_obj_split_dirt": result_obj_split_dirt,
            "results_acc": results_acc,
            "img_url": "/media/classify_img/" + image_file,
            "latest_log": latest_log,
        }
    else:
        context = {
            "img_url": "/media/classify_img/" + image_file,
            "results_acc": results_acc,
        }

    return render(request, "classify/classify_result.html", context)
