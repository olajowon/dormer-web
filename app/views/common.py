# Created by zhouwang on 2020/12/19.
from django.http import HttpResponse
from rest_framework.views import APIView
from ..handlers.common import Common
from ..utils.request import with_request


class Render(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        resp_headers, resp_content = Common().render(request.query_params)
        resp = HttpResponse(resp_content)
        for k, v in resp_headers.items():
            resp.__setitem__(k, v)
        return resp
