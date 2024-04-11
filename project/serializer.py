from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from utilities.serializer_helper import CustomSlugRelatedField
from .models import Project, Room, BoardType, Board, NodeType, Device, HardwareScenario, Node, SoftwareScenario


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('user',)


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BoardTypeSerializer(ModelSerializer):
    class Meta:
        model = BoardType
        fields = '__all__'


class ProjectBoardsSerializer(ModelSerializer):
    control_sms_board = CustomSlugRelatedField(slug_field='name', queryset=Board.objects.all(), required=False)
    control_wifi_board = CustomSlugRelatedField(slug_field='name', queryset=Board.objects.all(), required=False)

    class Meta:
        model = Board
        fields = '__all__'

    # def validate(self, attrs):
    #     if attrs['board_type'] != '1' or attrs['board_type'] != '2':
    #         print('ssss')
    #         print(attrs)
    #         if attrs['control_sms_board'] or attrs['control_wifi_board']:
    #             return attrs
    #         raise ValidationError('لطفا برد پیامکی یا وای فای کنترل کننده را مشخص نمایید')
    #     return attrs


class NodeTypeSerializer(ModelSerializer):
    class Meta:
        model = NodeType
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['name'] == '0':
            representation['name'] = 'کلید تک تایمر'
        elif representation['name'] == '1':
            representation['name'] = 'سنسور دما'
        elif representation['name'] == '2':
            representation['name'] = 'سنسور رطوبت'
        elif representation['name'] == '3':
            representation['name'] = 'سنسور گاز'
        elif representation['name'] == '4':
            representation['name'] = 'سنسور خاک'
        elif representation['name'] == '5':
            representation['name'] = 'دیمر'
        elif representation['name'] == '6':
            representation['name'] = 'کلید سه تایمر'
        elif representation['name'] == '7':
            representation['name'] = 'چشمی ها و سنسور تشخیص حرکت'

        return representation


class NodeProjectSerializer(ModelSerializer):
    # node_type = CustomSlugRelatedField(slug_field='name', queryset=NodeType.objects.all())
    # board_project = CustomSlugRelatedField(slug_field='unique_id', queryset=ProjectBoards.objects.all())

    class Meta:
        model = Node
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['node_type'] == '0':
            representation['node_type'] = 'کلید تک تایمر'
        elif representation['node_type'] == '1':
            representation['node_type'] = 'سنسور دما'
        elif representation['node_type'] == '2':
            representation['node_type'] = 'سنسور رطوبت'
        elif representation['node_type'] == '3':
            representation['node_type'] = 'سنسور گاز'
        elif representation['node_type'] == '4':
            representation['node_type'] = 'سنسور خاک'
        elif representation['node_type'] == '5':
            representation['node_type'] = 'دیمر'
        elif representation['node_type'] == '6':
            representation['node_type'] = 'کلید سه تایمر'
        elif representation['node_type'] == '7':
            representation['node_type'] = 'چشمی ها و سنسور تشخیص حرکت'

        return representation


class DeviceSerializer(ModelSerializer):
    node_project = NodeProjectSerializer()

    class Meta:
        model = Device
        fields = '__all__'


class DevicePostSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class HardwareScenarioSerializer(ModelSerializer):
    user = CustomSlugRelatedField(slug_field='username', queryset=get_user_model().objects.all(), required=False)

    class Meta:
        model = HardwareScenario
        fields = '__all__'
        depth = 0


class SoftwareScenarioSerializer(ModelSerializer):
    user = CustomSlugRelatedField(slug_field='username', queryset=get_user_model().objects.all(), required=False)

    class Meta:
        model = SoftwareScenario
        fields = '__all__'
        depth = 0
