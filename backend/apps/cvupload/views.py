from apps.cvupload.models import CvUploadinfo
from utils import serializers
from utils.common import getRandomSet
from utils.jsonResponse import SuccessResponse
from utils.viewset import CustomModelViewSet
from utils.serializers import CustomModelSerializer
from utils.filters import UsersCVManageTimeFilter


class CvUploadinfoManageSerializer(CustomModelSerializer):
    """
    简历上传部分用户管理-序列化器
    """

    class Meta:
        model = CvUploadinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvUploadinfoManageCreateSerializer(CustomModelSerializer):
    """
    简历创建管理-序列化器
    """

    class Meta:
        model = CvUploadinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvUploadinfoManageUpdateSerializer(CustomModelSerializer):
    """
    简历更新管理-序列化器
    """

    class Meta:
        model = CvUploadinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvUploadinfoViewSet(CustomModelViewSet):
    """
    简历文件上传管理接口:
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = CvUploadinfo.objects.all().order_by('-create_datetime')  # 按照创建时间排序
    serializer_class = CvUploadinfoManageSerializer
    create_serializer_class = CvUploadinfoManageCreateSerializer
    update_serializer_class = CvUploadinfoManageUpdateSerializer
    filterset_class = UsersCVManageTimeFilter

