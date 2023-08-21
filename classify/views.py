from django.shortcuts import render
from users.models import User, RecycleLog
from ultralytics import YOLO
import os
from users.models import RecycleLog

# Create your views here.

ai_model = YOLO("static/model/best.pt")


def test_yolo(request):
    # image_dir = RecycleLog.objects.get().input_img
    image_dir = "static/image/10349@3_01001_220715_P1_T1.jpg"
    image_file = image_dir.split("/")[-1]
    image_file_name = image_file.split(".")[0]
    print(image_file)
    print(image_file_name)
    if os.path.isfile("runs/detect/results/labels/" + image_file_name + ".txt"):
        os.remove("runs/detect/results/labels/" + image_file_name + ".txt")
    results = ai_model(
        "static/image/10349@3_01001_220715_P1_T1.jpg",
        save_txt=True,
        name="results",
        exist_ok=True,
    )

    txt_result = open("runs/detect/results/labels/" + image_file_name + ".txt", "r")
    print(txt_result.readlines())
    txt_result.close()

    context = {
        "results": results,
    }
    return render(request, "classify/test.html", context)
