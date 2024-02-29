"""
@Remark: 简历上传相关的的路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

from apps.cvupload.views import CvUploadinfoViewSet

system_url = routers.SimpleRouter()
system_url.register(r'cvupload', CvUploadinfoViewSet)

urlpatterns = [
    # re_path('cv_root/', CvinfoViewSet.as_view({'get': 'cv_root'})),
]
urlpatterns += system_url.urls
