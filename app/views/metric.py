# Created by zhouwang on 2020/11/7.
from rest_framework.views import APIView
from ..handlers.metric import Metric
from ..lib.request import with_request


class MetricCategories(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        data = Metric().get_metric_categories()
        return data


class MetricChildren(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        data = Metric().get_metric_children(request.query_params)
        return data


class MetricOffsprings(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        data = Metric().get_metric_offsprings(request.query_params)
        return data


class Render(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        data = Metric().render(request.query_params)
        return data
