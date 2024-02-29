from apps.cvtest.models import Cvinfo
from utils import serializers
from utils.common import getRandomSet
from utils.jsonResponse import SuccessResponse
from utils.viewset import CustomModelViewSet
from utils.serializers import CustomModelSerializer


class CvinfoManageSerializer(CustomModelSerializer):
    """
    简历列表管理-序列化器
    """

    class Meta:
        model = Cvinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvinfoManageCreateSerializer(CustomModelSerializer):
    """
    简历创建管理-序列化器
    """

    class Meta:
        model = Cvinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvinfoManageUpdateSerializer(CustomModelSerializer):
    """
    简历更新管理-序列化器
    """

    class Meta:
        model = Cvinfo
        fields = '__all__'
        read_only_fields = ["id"]


class CvinfoViewSet(CustomModelViewSet):
    """
    简历管理接口:
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Cvinfo.objects.all().order_by("-create_datetime")  # 按照创建时间排序
    serializer_class = CvinfoManageSerializer
    create_serializer_class = CvinfoManageCreateSerializer
    update_serializer_class = CvinfoManageUpdateSerializer

    # 重写delete方法，让它支持批量删除 如：  /api/admin/user/1,2,3/ 批量删除id 1，2，3得用户
    # 重写delete方法，并改为逻辑删除
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object_list()
        # instance为即将删除的用户
        # print("==========", instance[0].name)
        for i in range(len(instance)):
            randomstr = getRandomSet(4)
            instance[i].is_delete = True
            instance[i].name = instance[i].name + "(已删除)" + randomstr
            # instance[i].mobile = instance[i].mobile + "(已删除)" + randomstr
            instance[i].save()
        return SuccessResponse(data=[], msg="删除成功")

    # def cv_root(self, request):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     queryset = queryset.filter().order_by('id')
    #     serializer = CvinfoSerializer(queryset, many=True)
    #     return CvinfoSerializer(data=serializer.data, msg="获取成功")
