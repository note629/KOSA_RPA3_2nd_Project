from django.shortcuts import render


def storemap_view(request):
    return render(request, "storemap/zerobasemap.html")
