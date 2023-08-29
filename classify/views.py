import math
import os
import shutil

from django.http import HttpResponse
from django.shortcuts import render, redirect
from ultralytics import YOLO
from urllib.parse import quote, unquote

from activity.models import GalleryLog, GalleryLikes
from classify.forms import ClassifyForm
from users.models import RecycleLog


ai_model = YOLO("static/model/best.pt")

classify_list = [
    "철캔_훼손 안 됨_이물질 없음",
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
    "페트병(무색)_훼손 안 됨_이물질 없음",
    "페트병(무색)_훼손 안 됨_이물질 있음",
    "페트병(무색)_훼손됨_이물질 없음",
    "페트병(무색)_훼손됨_이물질 있음",
    "페트병(유색)_훼손 안 됨_이물질 없음",
    "페트병(유색)_훼손 안 됨_이물질 있음",
    "페트병(유색)_훼손됨_이물질 없음",
    "페트병(유색)_훼손됨_이물질 있음",
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

classify_result = [
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "재활용 불가능",
    "재활용 가능",
    "재활용 불가능",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 불가능",
    "재활용 불가능",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 불가능",
    "재활용 불가능",
    "재활용 가능",
    "이물질 제거 필요",
    "재활용 불가능",
    "재활용 불가능",
]

classify_detail = [
    # 0~7
    "담배꽁초 등 이물질을 넣지 않고 배출합니다_플라스틱 뚜껑 등 금속캔과 다른 재질은 제거한 후 배출합니다",
    # 8~11
    "물기에 젖지 않도록 하고, 반듯하게 펴서 차곡차곡 쌓은 후 흩날리지 않도록 끈 등으로 묶어서 배출합니다_스프링 등 종이류와 다른 재질은 제거한 후 배출합니다_테이프 등 종이류와 다른 재질은 제거한 후 배출합니다_이외의 종이 쓰레기는 쓰레기 종량제 봉투로 배출하세요",
    # 12~31
    "부착상표, 부속품 등 본체와 다른 재질은 제거한 후 배출합니다_부착상표는 쓰레기 종량제 봉투로 배출하세요",
    # 32~35
    "부착상표 등 스티로폼과 다른 재질은 제거한 후 배출합니다_전자제품 구입 시 완충재로 사용되는 발포합성수지 포장재는 가급적 구입처로 반납합니다",
    # 36~39
    "흩날리지 않도록 봉투에 담아 배출합니다",
    # 40~51
    "담배꽁초 등 이물질을 넣지 않고 배출합니다_유리병이 깨지지 않도록 주의하여 배출합니다_소주, 맥주 등 빈용기보증금 대상 유리병은 소매점 등으로 반납하여 보증금 환급받을 수 있습니다",
]


def image_upload(request):
    if not request.user.is_authenticated:
        return redirect("users:login_view")

    if request.user.is_authenticated:
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
            "form": form,
            "page_title": "분류 이미지 업로드",
        }
        return render(request, "classify/classify.html", context)


def classify_yolo(request):
    if not request.user.is_authenticated:
        return redirect("users:login_view")

    if request.user.is_authenticated:
        latest_log = (
            RecycleLog.objects.filter(user_id=request.user.id)
            .order_by("-use_date")
            .first()
        )
        # /media/recycle_img/374745_01002_220728_P1_T1.jpg
        # print(latest_log.input_img.url)
        image_url = latest_log.input_img.url
        image_file = image_url.split("/")[-1]
        image_file_name = image_file.split(".")[0]
        print(image_file)
        print(image_file_name)
        if os.path.isfile("runs/detect/results/labels/" + image_file_name + ".txt"):
            os.remove("runs/detect/results/labels/" + image_file_name + ".txt")
        copied_url = "media/recycle_img_copy/" + image_file
        print(unquote(image_url))
        print(quote(copied_url))
        shutil.copy(unquote(image_url[1:]), quote(copied_url))
        results = ai_model(
            quote(copied_url),
            save_txt=True,
            save_conf=True,
            # conf=0.5,
            save=True,
            name="results",
            exist_ok=True,
        )

        from_file_path = "runs/detect/results/" + image_file  # 복사할 파일
        to_file_path = "media/classify_img/" + image_file  # 복사 위치 및 파일 이름 지정
        shutil.copy(quote(from_file_path), unquote(to_file_path))

        if os.path.isfile(
            quote("runs/detect/results/labels/" + image_file_name + ".txt")
        ):
            os.rename(
                quote("runs/detect/results/labels/" + image_file_name + ".txt"),
                unquote("runs/detect/results/labels/" + image_file_name + ".txt"),
            )
            txt_result = open(
                unquote("runs/detect/results/labels/" + image_file_name + ".txt"), "r"
            )
            # print(txt_result.readlines())
            result_list = [line for line in txt_result.readlines()]
            txt_result.close()
            result_list_split_obj = int((result_list[0].split(" "))[0])
            result_list_split_acc = (result_list[0].split(" "))[-1]

            result_obj = classify_list[int(result_list_split_obj)]
            result_obj_split_name = (result_obj.split("_"))[0]
            result_obj_split_damg = (result_obj.split("_"))[1]
            result_obj_split_dirt = (result_obj.split("_"))[2]
            results_acc = round(float(result_list_split_acc) * 100, 2)

            if float(result_list_split_acc) > 0.7:
                latest_log.classify_item = str(result_list_split_obj)
                latest_log.save()

                results_classify = classify_result[int(result_list_split_obj)].split(
                    "_"
                )
                print(results_classify)

                if result_list_split_obj >= 0 and result_list_split_obj <= 7:
                    results_tip = classify_detail[0].split("_")
                elif result_list_split_obj >= 8 and result_list_split_obj <= 11:
                    results_tip = classify_detail[1].split("_")
                elif result_list_split_obj >= 12 and result_list_split_obj <= 31:
                    results_tip = classify_detail[2].split("_")
                elif result_list_split_obj >= 32 and result_list_split_obj <= 35:
                    results_tip = classify_detail[3].split("_")
                elif result_list_split_obj >= 36 and result_list_split_obj <= 39:
                    results_tip = classify_detail[4].split("_")
                elif result_list_split_obj >= 40:
                    results_tip = classify_detail[5].split("_")
                print(results_tip)
                print(image_file)

                # txt_result.close()
                context = {
                    "result_obj_split_name": result_obj_split_name,
                    "result_obj_split_damg": result_obj_split_damg,
                    "result_obj_split_dirt": result_obj_split_dirt,
                    "results_acc": results_acc,
                    "results_classify": results_classify[0],
                    "results_tip": results_tip,
                    "img_url": unquote("/media/classify_img/" + image_file),
                    "latest_log": latest_log,
                    "page_title": "분류 결과",
                }
            else:
                context = {
                    "img_url": unquote("/media/classify_img/" + image_file),
                    "results_acc": results_acc,
                }
        else:
            context = {
                "img_url": unquote("/media/classify_img/" + image_file),
                "results_acc": 0.0,
            }

    return render(request, "classify/classify_result.html", context)


def upload_to_gallery(request):
    if request.user.is_authenticated:
        latest_recycle_log = (
            RecycleLog.objects.filter(user_id=request.user.id)
            .order_by("-use_date")
            .first()
        )
        user_id = request.user.id
        recyclelog_id = latest_recycle_log.id

        # 이미 GalleryLog가 있는지 확인합니다.
        existing_gallery_log = GalleryLog.objects.filter(
            recyclelog_id=recyclelog_id
        ).first()

        if existing_gallery_log is None:
            # 없다면 새로 생성합니다.
            GalleryLog.objects.create(user_id=user_id, recyclelog_id=recyclelog_id)

            latest_gallery_log = (
                GalleryLog.objects.filter(user=request.user).order_by("-id").first()
            )

            gallerylog_id = latest_gallery_log.id

            # 이미 GalleryLikes가 있는지 확인합니다.
            existing_likes = GalleryLikes.objects.filter(
                gallerylog_id=gallerylog_id
            ).first()

            # if existing_likes is None:
            #     # 없다면 새로 생성합니다.
            #     GalleryLikes.objects.create(
            #         user_id=user_id, gallerylog_id=gallerylog_id
            #     )

        return redirect("activity:gallery_view")  # activity 앱의 gallery라는 이름의 URL로 리다이렉트
    else:
        return HttpResponse("Upload failed")
