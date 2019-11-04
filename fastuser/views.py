from rest_framework.response import Response
from rest_framework.views import APIView
from fastuser.common import response
from fastuser import models
from fastuser import serializers
import logging
import json
# Create your views here.
from fastuser.common.token import generate_token
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from fastrunner.utils.crypto_aes import crypto_aes

logger = logging.getLogger('FastRunner')


class RegisterView(APIView):

    authentication_classes = ()
    permission_classes = ()

    """
    注册:{
        "user": "demo"
        "password": "1321"
        "email": "1@1.com"
    }
    """

    def post(self, request):
        # 对加密的请求数据进行解密
        try:
            requestData = crypto_aes().decrypt_text(request.data["requestData"])
            requestData_obj = json.loads(requestData)
        except KeyError:
            return Response(response.CRYPTO_AES_ERROR)
        try:
            username = requestData_obj["username"]
            password = requestData_obj["password"]
            email = requestData_obj["email"]
        except KeyError:
            return Response(response.KEY_MISS)

        if models.UserInfo.objects.filter(username=username).first():
            return Response(response.REGISTER_USERNAME_EXIST)

        if models.UserInfo.objects.filter(email=email).first():
            return Response(response.REGISTER_EMAIL_EXIST)
        
        # 此处需要将解密后的用户名及邮箱，加密后的密码存到数据库表中
        requestData_obj["password"] = make_password(password)
        serializer = serializers.UserInfoSerializer(data=requestData_obj)

        if serializer.is_valid():
            serializer.save()
            return Response(response.REGISTER_SUCCESS)
        else:
            return Response(response.SYSTEM_ERROR)


class LoginView(APIView):
    """
    登陆视图，用户名与密码匹配返回token
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        用户名密码一致返回token
        {
            username: str
            password: str
        }
        """
        # 对加密的请求数据进行解密
        try:
            print(request.data)
            requestData = crypto_aes().decrypt_text(request.data["requestData"])
            requestData_obj = json.loads(requestData)
        except KeyError:
            return Response(response.CRYPTO_AES_ERROR)
        try:
            username = requestData_obj["username"]
            password = requestData_obj["password"]
        except KeyError:
            return Response(response.KEY_MISS)

        user = models.UserInfo.objects.filter(username=username).first()

        if not user:
            return Response(response.USER_NOT_EXISTS)

        if not check_password(password, user.password):
            return Response(response.LOGIN_FAILED)

        token = generate_token(username)

        try:
            models.UserToken.objects.update_or_create(user=user, defaults={"token": token})
        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)
        else:
            response.LOGIN_SUCCESS["token"] = token
            response.LOGIN_SUCCESS["user"] = username
            return Response(response.LOGIN_SUCCESS)


class ChangePwdView(APIView):
    authentication_classes = ()
    permission_classes = ()

    """
    注册:{
        "username": "demo"
        "old_password": "@demo1234"
        "new_password": "@demo12345678"
    }
    """

    def post(self, request):
        # 对加密的请求数据进行解密
        try:
            requestData = crypto_aes().decrypt_text(request.data["requestData"])
            requestData_obj = json.loads(requestData)
        except KeyError:
            return Response(response.CRYPTO_AES_ERROR)
        try:
            username = requestData_obj["username"]
            old_password = requestData_obj["old_password"]
            new_password = requestData_obj["new_password"]
        except KeyError:
            return Response(response.KEY_MISS)

        user = models.UserInfo.objects.filter(username=username).first()
        print(username)
        print(old_password)
        print(new_password)
        if not user:
            return Response(response.USER_NOT_EXISTS)

        if not check_password(old_password, user.password):
            return Response(response.USER_PWD_ERROR)
        try:
            # 此处需要将解密后的用户名及邮箱，加密后的密码存到数据库表中
            requestData_obj["password"] = make_password(new_password)
            models.UserInfo.objects.filter(username=username).update(password=requestData_obj["password"])
            return Response(response.CHANGE_PWD_SUCCESS)
        except BaseException:
            return Response(response.SYSTEM_ERROR)
