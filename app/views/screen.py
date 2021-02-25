# Created by zhouwang on 2021/2/8.

from rest_framework.views import APIView
from ..handlers.screen import Screen as ScreenHdl
from ..utils.request import with_request


class ScreenDashboard(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        path = kwargs.get('path')
        data = ScreenHdl(request.user).get_screen_dashboard(path)
        return data


class ScreenSettings(APIView):
    @with_request(auth=True)
    def put(self, request, *args, **kwargs):
        path = kwargs.get('path')
        data = ScreenHdl(request.user).update_screen_settings(path, request.data)
        return data
