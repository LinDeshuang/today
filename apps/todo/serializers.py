#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Lindes
"""
from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    finish_level = serializers.HiddenField(default=0)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = Todo
        fields = ['id', 'title', 'content', 'user', 'file', 'finish_level', 'level', 'add_time']

