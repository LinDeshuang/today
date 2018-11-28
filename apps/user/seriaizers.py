#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Lindes
"""
import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from rest_framework.validators import UniqueValidator

from .models import VerifyCode

User = get_user_model()


class SendEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)

    def validate_email(self, email):
        """
        验证邮箱的合法性
        :param email:
        :return:
        """
        # 验证邮箱格式是否合法
        if not re.match(r'^\w+@+\w+\.\w+$', email):
            raise serializers.ValidationError("邮箱格式错误")

        # 验证邮箱是否已经注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("邮箱已被注册")

        # 验证发送频率限制
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, target=email).first():
            raise serializers.ValidationError("距离上次发送未超过60秒")

        return email


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=6, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, help_text="验证码"
                                 )
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户名已存在")])
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True)

    # 验证码验证
    def validate_code(self, code):
        verify_record = VerifyCode.objects.filter(target=self.initial_data['username']).order_by('-add_time').first()
        if verify_record:
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > verify_record.add_time:
                print(five_minutes_ago)
                print(verify_record.add_time)
                raise serializers.ValidationError("验证码已失效")
            if verify_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs['email'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "password")
