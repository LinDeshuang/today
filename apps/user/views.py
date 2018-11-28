from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .models import VerifyCode
from .seriaizers import SendEmailSerializer, UserRegSerializer, UserDetailSerializer
from .utils import SendMail

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SendEmailViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码
    """
    serializer_class = SendEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        send_res = SendMail(to_email=email)

        print(send_res)
        if not send_res:
            return Response({
                "email": "邮箱验证码发送失败，请重试！"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=send_res, target=email)
            code_record.save()
            return Response({
                "email": email
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            return []
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data

        payload = jwt_payload_handler(user)

        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


