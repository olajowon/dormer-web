# Created by zhouwang on 2021/2/25.

from rest_framework import serializers


class Serializer:
    def __new__(cls, *args, **kwargs):
        class S(serializers.ModelSerializer):
            class Meta:
                model = args[0].__class__
                fields = '__all__'
        return S(*args, **kwargs)
