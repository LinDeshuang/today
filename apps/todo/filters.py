#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Lindes
"""
import django_filters
from .models import Todo


class TodoFilters(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name='add_time')

    class Meta:
        model = Todo
        fields = ['date']
