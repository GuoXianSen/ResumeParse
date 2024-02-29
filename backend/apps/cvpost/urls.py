"""
@Remark: 简历相关的路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

from apps.cvpost.views import CvPostinfoViewSet

system_url = routers.SimpleRouter()
system_url.register(r'cvpost', CvPostinfoViewSet)

urlpatterns = [

]
urlpatterns += system_url.urls
