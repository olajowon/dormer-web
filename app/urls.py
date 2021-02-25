# Created by zhouwang on 2020/11/12.

from django.urls import path
from .views import metric, common, tree, screen

urlpatterns = [
    path('metric/metric_categories/', metric.MetricCategories.as_view()),
    path('metric/metric_children/', metric.MetricChildren.as_view()),
    path('metric/metric_offsprings/', metric.MetricOffsprings.as_view()),
    path('tree/nodes/', tree.Node.as_view()),
    path('tree/nodes/<str:node>/', tree.Node.as_view()),
    path('tree/nodes/<str:node>/users/', tree.NodeUsers.as_view()),
    path('tree/node_children/', tree.NodeChildren.as_view()),
    path('tree/node_user_role/', tree.NodeUserRole.as_view()),
    path('screen/screens/<str:path>/settings/', screen.ScreenSettings.as_view()),
    path('screen/screens/<str:path>/dashboard/', screen.ScreenDashboard.as_view()),
    path('render/', common.Render.as_view())
]
