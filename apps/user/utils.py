#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Lindes
"""
import random

from django.core.mail import send_mail


def GenCode(length):
    """
    生成验证码
    """
    res = ''
    for i in range(length):
        res += str(random.randint(0, 9))
    return res


def SendMail(to_email):
    """
    发送邮件验证码
    :param to_email:
    :return:
    """
    code = GenCode(6)
    res = send_mail(
        subject="Today小站",
        message=f"[Today小站]您好，欢迎来到Today小站，您的邮箱验证码是：{code}，有效期半个小时，请妥善保管！",
        from_email="18826131701@163.com",
        recipient_list=[to_email],
        fail_silently=False
    )
    print("send_res", res)
    if res:
        return code
    else:
        return None
