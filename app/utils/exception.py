# Created by zhouwang on 2019/9/30.


class ParamError(Exception):
    def __init__(self, key, message):
        self.key = key
        self.message = message
        self.error = {key: [message]}


class ForbiddenError(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class FormError(Exception):
    def __init__(self, errors):
        self.error = errors