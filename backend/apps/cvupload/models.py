from django.db import models
from utils.models import BaseModel, CoreModel
from mysystem.models import Users


class CvUploadinfo(CoreModel):
    """简历上传功能中的信息"""
    name = models.CharField(max_length=50, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')
    xueli = models.CharField(max_length=20, verbose_name='最高学历')
    school = models.CharField(max_length=20, verbose_name='毕业院校')
    nianxian = models.IntegerField(verbose_name='工作年限')
    major = models.CharField(max_length=20, verbose_name='专业')
    is_delete = models.BooleanField(default=False, blank=True, verbose_name='逻辑删除', help_text='逻辑删除')  # 非必填
    cv_img = models.CharField(max_length=255, verbose_name="简历图片URL", default="")
    cv_list = models.CharField(max_length=255, verbose_name="所有简历图片URL", default="")
    post = models.CharField(max_length=60, verbose_name="推荐岗位", default="", null=True, blank=True)
    match = models.CharField(max_length=255, verbose_name="岗位匹配度", default="", null=True, blank=True)

    class Meta:
        db_table = 'cv_upload_info'
        verbose_name = '简历上传信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
