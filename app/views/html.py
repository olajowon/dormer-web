# Created by zhouwang on 2020/11/7.
from django.shortcuts import render


def metric(request):
    return render(request, 'metric.html')
