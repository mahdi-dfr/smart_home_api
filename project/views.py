from django.db.models import Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .models import Project, Room, BoardType, ProjectBoards, NodeType, NodeProject, Device, ProjectScenario
from .permissions import IsUser
from .serializer import ProjectSerializer, RoomSerializer, BoardTypeSerializer, ProjectBoardsSerializer, \
    NodeTypeSerializer, NodeProjectSerializer, DeviceSerializer, ScenarioSerializer, DevicePostSerializer
from . import permissions


# Create your views here.

class ProjectView(ModelViewSet):
    permission_classes = [IsAuthenticated, permissions.IsUser]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ControlBoardView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        project = self.request.query_params['project']
        sms_queryset = ProjectBoards.objects.filter(project=project, board_type=1)
        wifi_queryset = ProjectBoards.objects.filter(project=project, board_type=2)

        # queryset = ProjectBoards.objects.filter(Q(Q(project=project, board_type=0) | Q(project=project, board_type=1)))
        sms_serializer = ProjectBoardsSerializer(instance=sms_queryset, many=True)
        wifi_serializer = ProjectBoardsSerializer(instance=wifi_queryset, many=True)
        return Response(data={'sms': sms_serializer.data, 'wifi': wifi_serializer.data})

    # permission_classes = [IsAuthenticated,]
    # serializer_class = ProjectBoardsSerializer
    # queryset = ProjectBoards.objects.all()
    #
    # def get_queryset(self):
    #     project = self.request.query_params['project']
    #     return ProjectBoards.objects.filter(Q(Q(project=project, board_type=0) | Q(project=project, board_type=1)))
    #
    # def get(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(instance=self.queryset)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)


class RoomView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        project_user = Project.objects.get(id=project_id).user
        if self.request.user == project_user:
            return Room.objects.filter(project=project_id)


class BoardTypeView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BoardType.objects.all()
    serializer_class = BoardTypeSerializer


class NodeTypeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = NodeType.objects.all()
    serializer_class = NodeTypeSerializer


class ProjectBoardsView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = ProjectBoards.objects.all()
    serializer_class = ProjectBoardsSerializer

    def perform_create(self, serializer):
        project = self.request.data['project']
        board = self.request.data['board_type']
        queryset = ProjectBoards.objects.filter(project=project, board_type=board)
        if queryset:
            last_item = queryset.last()
            unique_id = last_item.unique_id
            serializer.validated_data['unique_id'] = unique_id + 1
            serializer.save()
        serializer.save()

    def get_queryset(self):
        project = self.request.query_params.get('project')
        if project is not None:
            return ProjectBoards.objects.filter(project=project)
        return ProjectBoards.objects.all()


class NodeTypeView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = NodeType.objects.all()
    serializer_class = NodeTypeSerializer


class NodeProjectView(ModelViewSet):
    pagination_class = None
    permission_classes = [IsAuthenticated]
    queryset = NodeProject.objects.all()
    serializer_class = NodeProjectSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        board_project = ProjectBoards.objects.get(id=data['board_project'])
        board_type = board_project.board_type

        if board_type.name == '2':

            data_list = [
                {'node_type': 2, 'board_project': board_project.id, 'project': data['project'], 'is_active': False,
                 'unique_id': 1},
                {'node_type': 3, 'board_project': board_project.id, 'project': data['project'], 'is_active': False,
                 'unique_id': 1},
                {'node_type': 4, 'board_project': board_project.id, 'project': data['project'], 'is_active': False,
                 'unique_id': 1},
                {'node_type': 5, 'board_project': board_project.id, 'project': data['project'], 'is_active': False,
                 'unique_id': 1}
            ]
            for data_to_save in data_list:
                serializer = NodeProjectSerializer(data=data_to_save)
                if serializer.is_valid():
                    serializer.save()
            return Response(data='success', status=status.HTTP_201_CREATED)

        elif board_type.name == '3':
            for i in range(1, 13):
                relay_data = {'node_type': 1, 'board_project': board_project.id, 'project': data['project'],
                              'is_active': False,
                              'unique_id': i}
                serializer = NodeProjectSerializer(data=relay_data)
                if serializer.is_valid():
                    serializer.save()
            return Response(data='success', status=status.HTTP_201_CREATED)

        elif board_type.name == '4':
            dimmer_data = {'node_type': 6, 'board_project': board_project.id, 'project': data['project'],
                           'is_active': False,
                           'unique_id': 1}
            serializer = NodeProjectSerializer(data=dimmer_data)
            if serializer.is_valid():
                serializer.save()
                return Response(data='success', status=status.HTTP_201_CREATED)

        elif board_type.name == '0':
            for i in range(1, 3):
                relay_data = {'node_type': 7, 'board_project': board_project.id, 'project': data['project'],
                              'is_active': False,
                              'unique_id': i}
                serializer = NodeProjectSerializer(data=relay_data)
                if serializer.is_valid():
                    serializer.save()

            for i in range(1, 8):
                relay_data = {'node_type': 8, 'board_project': board_project.id, 'project': data['project'],
                              'is_active': False,
                              'unique_id': i}
                serializer = NodeProjectSerializer(data=relay_data)
                if serializer.is_valid():
                    serializer.save()

            return Response(data='success', status=status.HTTP_201_CREATED)

        return Response(data='failed')


class DeviceNodeViewSet(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        project = self.request.query_params['project']
        node = self.request.query_params['node']
        node_type = NodeType.objects.get(name=node)
        inactive_nodes = NodeProject.objects.filter(project=project, node_type=node_type.id, is_active=False)
        serializer = NodeProjectSerializer(instance=inactive_nodes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DeviceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filterset_fields = ['device_type']
    ordering_fields = "__all__"

    def perform_create(self, serializer):
        serializer.save()

        data = self.request.data
        node_project = data['node_project']
        node = NodeProject.objects.get(id=node_project)
        node.is_active = True
        node.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        device = Device.objects.get(id=instance.id)
        node_id = device.node_project.id
        node = NodeProject.objects.get(id=node_id)
        node.is_active = False
        node.save()

        instance.delete()

    def get_queryset(self):
        base_queryset = Device.objects.filter(project=self.request.query_params['project'])

        if 'type' in self.request.query_params:
            base_queryset = base_queryset.filter(device_type=self.request.query_params['type'])

        if self.request.method == 'GET' and 'room' in self.request.query_params:
            base_queryset = base_queryset.filter(room=self.request.query_params['room'])

        return base_queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeviceSerializer
        return DevicePostSerializer


class DeviceScenario(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = [PageNumberPagination]

    def get(self, request, *args, **kwargs):
        queryset = Device.objects.filter(Q(Q(device_type='0') | Q(device_type='6')))
        serializer = DeviceSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ScenarioViewSet(APIView):
    permission_classes = [IsAuthenticated, IsUser]
    pagination_class = None

    # queryset = ProjectScenario.objects.all()
    # serializer_class = ScenarioSerializer

    def post(self, request):
        data = request.data

        for i in data:
            serializer = ScenarioSerializer(data=i)
            if serializer.is_valid():
                serializer.save(user=request.user)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        project = self.request.query_params['project']
        type = self.request.query_params['type']
        queryset = ProjectScenario.objects.filter(user=request.user.id, project=project, type=type)
        serializer_class = ScenarioSerializer(instance=queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            scenario = ProjectScenario.objects.get(pk=pk, user=request.user.id)
            scenario.delete()
            return Response({'status': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
        except ProjectScenario.DoesNotExist:
            return Response({'error': 'Scenario not found'}, status=status.HTTP_404_NOT_FOUND)
