from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Blog, MsPost
from .serializers import BlogSerializer, MsPostSerializer
from .permissions import IsOwnerOrSuperUser, IsSuperUserOrReadOnly
from rest_framework.permissions import IsAuthenticated



class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrSuperUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrSuperUser, IsOwnerOrSuperUser]

class MsPostListCreateAPIView(generics.ListCreateAPIView):
    queryset = MsPost.objects.all().order_by('-created_at')
    serializer_class = MsPostSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MsPostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MsPost.objects.all()
    serializer_class = MsPostSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    