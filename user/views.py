from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from acu.user_permissions import IsOwnUser
from .models import User
from .serializer import RegisterSerializer, UserInfoSerializer


# Create your views here.

class UserManagement(ModelViewSet):
    permission_classes = [IsOwnUser, ]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class MeView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.request.user)
        return Response(serializer.data)


