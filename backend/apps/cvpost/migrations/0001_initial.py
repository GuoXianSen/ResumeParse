# Generated by Django 4.2 on 2023-04-18 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="cvPostinfo",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=utils.models.make_uuid,
                        help_text="Id",
                        max_length=100,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Id",
                    ),
                ),
                (
                    "modifier",
                    models.CharField(
                        blank=True,
                        help_text="修改人",
                        max_length=100,
                        null=True,
                        verbose_name="修改人",
                    ),
                ),
                (
                    "dept_belong_id",
                    models.CharField(
                        blank=True,
                        help_text="数据归属部门",
                        max_length=100,
                        null=True,
                        verbose_name="数据归属部门",
                    ),
                ),
                (
                    "update_datetime",
                    models.DateTimeField(
                        auto_now=True, help_text="修改时间", null=True, verbose_name="修改时间"
                    ),
                ),
                (
                    "create_datetime",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="创建时间",
                        null=True,
                        verbose_name="创建时间",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="姓名")),
                ("age", models.IntegerField(verbose_name="年龄")),
                ("xueli", models.CharField(max_length=20, verbose_name="最高学历")),
                ("school", models.CharField(max_length=20, verbose_name="毕业院校")),
                ("nianxian", models.IntegerField(verbose_name="工作年限")),
                ("major", models.CharField(max_length=20, verbose_name="专业")),
                (
                    "is_delete",
                    models.BooleanField(
                        blank=True, default=False, help_text="逻辑删除", verbose_name="逻辑删除"
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="岗位标题")),
                ("description", models.TextField(verbose_name="岗位描述")),
                ("requirements", models.TextField(verbose_name="岗位要求")),
                (
                    "salary",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="薪水"
                    ),
                ),
                ("location", models.CharField(max_length=100, verbose_name="工作地点")),
                (
                    "creator",
                    models.ForeignKey(
                        db_constraint=False,
                        help_text="创建人",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_query_name="creator_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建人",
                    ),
                ),
            ],
            options={
                "verbose_name": "职位信息",
                "verbose_name_plural": "职位信息",
                "db_table": "cvpost_info",
            },
        ),
    ]
