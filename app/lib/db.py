# Created by zhouwang on 2020/11/12.

from .utils import lock
import elasticsearch
import configure
import requests
#import taos


class Elasticsearch:
    _instance = None

    @lock
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            connect = elasticsearch.Elasticsearch(**configure.elasticsearch)
            Elasticsearch._instance = connect
        return Elasticsearch._instance


class GraphiteApi:
    def render(self, params):
        params['format'] = 'json'
        resp = requests.post('%s/render' % configure.graphite_api['host'], data=params)
        resp.raise_for_status()
        return resp.json()


# class TDengine:
#     _instance = None
#
#     @lock
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             connect = taos.connect(**configure.td)
#             TDengine._instance = connect
#         return TDengine._instance
