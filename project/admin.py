from django.contrib import admin
from .models import Project, BoardType, ProjectBoards, NodeType, Room, Device, NodeProject, ProjectScenario

# Register your models here.

admin.site.register(Project)
admin.site.register(BoardType)
admin.site.register(ProjectBoards)
admin.site.register(NodeType)
admin.site.register(NodeProject)
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(ProjectScenario)
