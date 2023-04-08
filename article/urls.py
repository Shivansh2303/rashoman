from django.urls import path,include
from .views import *

APP_NAME='article'

urlpatterns = [
    path('article-create/',ArticleListCreateAPIView.as_view(),name='article-register'),
    path('article-detail/',ArticleDetailDeleteUpdateAPIView.as_view(),name='article-detail'),
    path('article-comment/',CommentAPIView.as_view(),name='article-comment'),
    path('article-comment/<int:pk>/',CommmentDetail.as_view(),name='article-comment-detail'),
]
