from django.contrib import admin
from .models import Project, BoardType, Board, NodeType, Room, Device, Node, HardwareScenario, SoftwareScenario

# Register your models here.

admin.site.register(Project)
admin.site.register(BoardType)
admin.site.register(Board)
admin.site.register(NodeType)
admin.site.register(Node)
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(HardwareScenario)
admin.site.register(SoftwareScenario)
