from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)








