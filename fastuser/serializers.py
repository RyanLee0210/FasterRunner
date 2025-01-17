from rest_framework import serializers
from fastuser import models


class UserInfoSerializer(serializers.Serializer):
    """
    用户信息序列化
    建议实现其他方法，否则会有警告
    """
    username = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "用户名校验失败"
    })

    password = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "密码校验失败"
    })

    email = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "邮箱校验失败"
    })

    def create(self, validated_data):
        """
        实现create方法
        """
        return models.UserInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('email', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        # 更新暂时先不实现
        return instance

