from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permission import IsOwnerOrReadOnly
from .models import Todo
from .filters import TodoFilters
from .serializers import TodoSerializer
from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    ListModelMixin

User = get_user_model()


class TodoPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class TodoViewset(ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    pagination_class = TodoPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = TodoFilters
    search_fields = ('title', 'content', 'level', 'finish_level')
    ordering_fields = ('level', 'finish_level')
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)