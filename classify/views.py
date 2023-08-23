import os

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
        "철캔_훼손X_오염X",
        "철캔_훼손X_오염O",
        "철캔_훼손O_오염X",
        "철캔_훼손O_오염O",
        "알루미늄캔_훼손X_오염X",
        "알루미늄캔_훼손X_오염O",
        "알루미늄캔_훼손O_오염X",
        "알루미늄캔_훼손O_오염O",
        "종이_훼손X_오염X",
        "종이_훼손X_오염O",
        "종이_훼손O_오염X",
        "종이_훼손O_오염O",
        "패트병(무색)_훼손X_오염X",
        "패트병(무색)_훼손X_오염O",
        "패트병(무색)_훼손O_오염X",
        "패트병(무색)_훼손O_오염O",
        "패트병(유색)_훼손X_오염X",
        "패트병(유색)_훼손X_오염O",
        "패트병(유색)_훼손O_오염X",
        "패트병(유색)_훼손O_오염O",
        "플라스틱(PE)_훼손X_오염X",
        "플라스틱(PE)_훼손X_오염O",
        "플라스틱(PE)_훼손O_오염X",
        "플라스틱(PE)_훼손O_오염O",
        "플라스틱(PP)_훼손X_오염X",
        "플라스틱(PP)_훼손X_오염O",
        "플라스틱(PP)_훼손O_오염X",
        "플라스틱(PP)_훼손O_오염O",
        "플라스틱(PS)_훼손X_오염X",
        "플라스틱(PS)_훼손X_오염O",
        "플라스틱(PS)_훼손O_오염X",
        "플라스틱(PS)_훼손O_오염O",
        "스티로폼_훼손X_오염X",
        "스티로폼_훼손X_오염O",
        "스티로폼_훼손O_오염X",
        "스티로폼_훼손O_오염O",
        "비닐_훼손X_오염X",
        "비닐_훼손X_오염O",
        "비닐_훼손O_오염X",
        "비닐_훼손O_오염O",
        "유리(갈색)_훼손X_오염X",
        "유리(갈색)_훼손X_오염O",
        "유리(갈색)_훼손O_오염X",
        "유리(갈색)_훼손O_오염O",
        "유리(녹색)_훼손X_오염X",
        "유리(녹색)_훼손X_오염O",
        "유리(녹색)_훼손O_오염X",
        "유리(녹색)_훼손O_오염O",
        "유리(녹색)_훼손X_오염X",
        "유리(녹색)_훼손X_오염O",
        "유리(녹색)_훼손O_오염X",
        "유리(녹색)_훼손O_오염O",
    ]

    latest_log = (
        RecycleLog.objects.filter(user_id=request.user.id).order_by("-use_date").first()
    )  # /media/recycle_img/374745_01002_220728_P1_T1.jpg

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
        save=True,
        name="results",
        exist_ok=True,
    )

    txt_result = open("runs/detect/results/labels/" + image_file_name + ".txt", "r")
    # print(txt_result.readlines())
    result_list = [line for line in txt_result.readlines()]
    result_list_split = (result_list[0].split(" "))[0]
    txt_result.close()

    context = {
        "results": classify_list[int(result_list_split)],
    }
    return render(request, "classify/classify_result.html", context)
