import random

from django.shortcuts import render
from users.models import RecycleLog
from random import randrange

from users.models import RecycleLog


def storemap_view(request):
    #################################
    #### (임시 Dummy Data 생성 user_id 값은 로그인 되어 있는 user_id로 생성됨)
    #
    # if request.user.is_authenticated:
    #     for classify_item_num in range(0, 52):
    #         for used_classify in range(randrange(2, 7)):
    #             obj = RecycleLog(
    #                 user_id=request.user.id,
    #                 input_img="recycle_img/242135_01001_220720_P1_T1.jpg",
    #                 classify_item=str(classify_item_num),
    #             )
    #             obj.save()
    #################################
    return render(request, "storemap/zerobasemap.html")
