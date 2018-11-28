#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Lindes
"""
import xadmin
from xadmin import views
from .models import Todo


class TodoAdmin(object):
    list_display = ['title', 'user', 'content', 'add_time', 'level', 'finish_level']


xadmin.site.register(Todo, TodoAdmin)
