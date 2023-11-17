from rest_framework.serializers import ModelSerializer
from .models import Project, Room, BoardType, ProjectBoards, NodeType, Device, ProjectScenario, NodeProject


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

    class Meta:
        model = ProjectBoards
        fields = '__all__'


class NodeTypeSerializer(ModelSerializer):
    class Meta:
        model = NodeType
        fields = '__all__'


class NodeProjectSerializer(ModelSerializer):
    class Meta:
        model = NodeProject
        fields = '__all__'


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class ScenarioSerializer(ModelSerializer):
    class Meta:
        model = ProjectScenario
        fields = '__all__'
