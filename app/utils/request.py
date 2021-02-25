# Created by zhouwang on 2020/11/13.
from django.http import JsonResponse, HttpResponse
from .exception import ParamError, ForbiddenError, NotFoundError, FormError
import traceback
import logging
logger = logging.getLogger('base')


def with_request(auth=False, perm=None):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            # 检查是否登录
            if auth and not request.user.is_authenticated:
                resp_data = {'msg': '未登录'}
                return JsonResponse(resp_data, status=401)

            # 检查权限
            if perm is None or request.user.has_perm(perm):
                try:
                    ret = func(self, request, *args, **kwargs)
                    if isinstance(ret, HttpResponse):
                        resp = ret
                    else:
                        resp = JsonResponse({'data': ret})
                except ParamError as e:
                    resp = JsonResponse({'msg': '参数无效', 'detail': str(e.message), 'error': e.error}, status=400)
                except FormError as e:
                    resp = JsonResponse({'msg': '参数无效', 'detail': '%s等参数无效' % list(e.error.keys()),
                                         'error': e.error}, status=400)
                except ForbiddenError as e:
                    resp = JsonResponse({'msg': '被禁止', 'detail': str(e.message)}, status=403)
                except NotFoundError as e:
                    resp = JsonResponse({'msg': str(e.message)}, status=404)
                except Exception as e:
                    logger.error('request error, uri: %s, msg: %s' % (request.path, traceback.format_exc()))
                    resp = JsonResponse({'msg': '内部错误', 'detail': str(e)}, status=500)
            else:
                resp = JsonResponse({'msg': '被禁止', 'detail': '没有访问权限 [%s]' % perm}, status=403)
            return resp
        return wrapper
    return decorator
