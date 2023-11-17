from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .serializer import RegisterSerializer


# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True, )
        serializer.save()

        return Response(status=HTTP_201_CREATED, data={"status": "success"})
