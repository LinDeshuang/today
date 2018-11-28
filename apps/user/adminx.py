#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Lindes
"""
import xadmin
from xadmin import views
from .models import VerifyCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "Today后台"
    site_footer = "Today"
    menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'target', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)