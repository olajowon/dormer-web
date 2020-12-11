# Created by zhouwang on 2020/11/12.

from django.urls import path
from .views import metric

urlpatterns = [
    path('metric/metric_categories/', metric.MetricCategories.as_view()),
    path('metric/metric_children/', metric.MetricChildren.as_view()),
    path('metric/metric_offsprings/', metric.MetricOffsprings.as_view()),
    path('metric/render/', metric.Render.as_view())
]
