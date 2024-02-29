"""
@Remark: 简历相关的路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

from apps.cvtest.views import CvinfoViewSet

system_url = routers.SimpleRouter()
system_url.register(r'cv', CvinfoViewSet)

urlpatterns = [
    # re_path('cv_root/', CvinfoViewSet.as_view({'get': 'cv_root'})),
]
urlpatterns += system_url.urls
