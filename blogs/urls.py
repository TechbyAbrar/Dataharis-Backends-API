from django.urls import path
from .views import BlogListCreateView, BlogDetailView, MsPostListCreateAPIView, MsPostRetrieveUpdateDestroyAPIView



urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    # path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('ms-posts/', MsPostListCreateAPIView.as_view(), name='post-list-create'),
    path('ms-posts/<int:pk>/', MsPostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
]

