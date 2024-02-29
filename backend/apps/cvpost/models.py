from django.db import models
from utils.models import BaseModel, CoreModel
from mysystem.models import Users


class cvPostinfo(CoreModel):
    """职位信息"""

    title = models.CharField(max_length=100, verbose_name='岗位名称')
    description = models.TextField(verbose_name="岗位描述")
    requirements = models.TextField(verbose_name='岗位要求')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='薪水')
    location = models.CharField(max_length=100, verbose_name='工作地点')

    class Meta:
        db_table = 'cvpost_info'
        verbose_name = '职位信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
