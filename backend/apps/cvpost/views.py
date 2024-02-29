from apps.cvpost.models import cvPostinfo
from utils import serializers
from utils.common import getRandomSet
from utils.jsonResponse import SuccessResponse
from utils.viewset import CustomModelViewSet
from utils.serializers import CustomModelSerializer


class CvPostinfoManageSerializer(CustomModelSerializer):
    """
    简历列表管理-序列化器
    """

    class Meta:
        model = cvPostinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvPostinfoManageCreateSerializer(CustomModelSerializer):
    """
    简历创建管理-序列化器
    """

    class Meta:
        model = cvPostinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvPostinfoManageUpdateSerializer(CustomModelSerializer):
    """
    简历更新管理-序列化器
    """

    class Meta:
        model = cvPostinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvPostinfoViewSet(CustomModelViewSet):
    """
    简历职位管理接口:
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = cvPostinfo.objects.all().order_by("-create_datetime")  # 按照创建时间排序
    serializer_class = CvPostinfoManageSerializer
    create_serializer_class = CvPostinfoManageCreateSerializer
    update_serializer_class = CvPostinfoManageUpdateSerializer



