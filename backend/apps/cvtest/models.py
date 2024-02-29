from django.db import models
from utils.models import BaseModel, CoreModel
from mysystem.models import Users


class Cvinfo(CoreModel):
    """简历信息"""
    name = models.CharField(max_length=50, verbose_name='姓名')
    age = models.IntegerField( verbose_name='年龄')
    xueli = models.CharField(max_length=20, verbose_name='最高学历')
    school = models.CharField(max_length=20, verbose_name='毕业院校')
    nianxian = models.IntegerField(verbose_name='工作年限')
    major = models.CharField(max_length=20, verbose_name='专业')
    is_delete = models.BooleanField(default=False, blank=True, verbose_name='逻辑删除', help_text='逻辑删除')  # 非必填

    # parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
    #                            verbose_name='上级行政区划')  # 外键链接自己
    # status = models.BooleanField(default=True, verbose_name="状态")

    # related_name='subs' ，意思为如果想找自己的子级，就可以通过area.subs找到自己下级所有的area区域,我们也可以这样调用获取市: area.area_set.all() ==> area.subs.all()
    # on_delete=models.SET_NULL:  如果省删掉了,省内其他的信息为 NULL
    class Meta:
        db_table = 'cv_info'
        verbose_name = '简历信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
