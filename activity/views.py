from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, RecycleLog

# Create your views here.


def activity_main(request):
    context = {}
    return render(request, "activity/maintest.html", context)


def user_rank(request):
    # 전체 유저 객체 획득
    users = User.objects.all()

    # 전체 유저 객체에 대한 로그 수와 유저 이름을 담는 리스트 생성 및 삽입
    all_user_rank_list = []
    for user in users:
        all_user_rank_list.append(
            [
                user.recyclelog_set.all().count(),
                user.username,
                user.recyclelog_set.all().order_by("-use_date").first(),
            ]
        )

    # 로그 수와 이름 담은 리스트를 오름차순 정렬을 통해 순위 결정
    all_user_rank_list = sorted(all_user_rank_list, key=lambda x: x[0], reverse=True)
    # print(all_user_rank_list)

    # 리스트 수가 10개가 넘으면 10번째까지로 리스트 슬라이싱
    if len(all_user_rank_list) > 10:
        all_user_rank_list = all_user_rank_list[:10]

    # 현재 유저 접속 상태에 따라 다른 context 전달
    # 유저 접속한 상태면 해당 유저의 랭크를 context에 포함
    # 유저가 접속하지 않은 상태면 모든 유저의 랭크만 전달
    current_user = request.user
    if current_user.is_authenticated:
        current_user_data = [
            current_user.recyclelog_set.all().count(),
            current_user.username,
            current_user.recyclelog_set.all().order_by("-use_date").first(),
        ]
        current_user_rank = all_user_rank_list.index(current_user_data)
        # print(current_user_rank)
        context = {
            "all_user_rank_list": all_user_rank_list,
            "current_user_data": current_user_data,
            "current_user_rank": current_user_rank + 1,
        }
    else:
        context = {
            "all_user_rank_list": all_user_rank_list,
        }

    return render(request, "activity/ranktest.html", context)
