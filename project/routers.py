from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectView, BoardTypeView, ProjectBoardsView, RoomView, ControlBoardView, NodeProjectView, \
    NodeTypeViewSet, DeviceNodeViewSet, DeviceViewSet, ScenarioViewSet, DeviceScenario

router = DefaultRouter()
router.register('project', ProjectView, basename='project')
router.register('board_type', BoardTypeView, basename='board_type')
router.register('node_type', NodeTypeViewSet, basename='node_type')
router.register('project_board', ProjectBoardsView, basename='project_board')
router.register('room', RoomView, basename='room')
router.register('node_project', NodeProjectView, basename='room')
router.register('device', DeviceViewSet, basename='device')
# router.register('scenario', ScenarioViewSet, basename='scenario')

urlpatterns = [
    path('control_boards/', ControlBoardView.as_view(), name='control_boards'),
    path('device_nodes/', DeviceNodeViewSet.as_view(), name='device_nodes'),
    path('device_scenario/', DeviceScenario.as_view(), name='device_scenario'),
    path('scenario/', ScenarioViewSet.as_view(), name='scenario'),
              ] + router.urls
