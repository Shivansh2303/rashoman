from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from DjangoBlog.permission import IsOwnerOrReadOnly

from django.shortcuts import render,get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset=Article.objects.all()
    serializer_class=ArticleSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ArticleDetailDeleteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Article.objects.all()
    serializer_class=ArticleSerializer
    lookup_field='pk'
    permission_classes=[IsAuthenticated,IsOwnerOrReadOnly]
    
class CommentAPIView(generics.ListCreateAPIView):
    serializer_class=CommentSerializer
    queryset=Comment.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    
class CommmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    queryset=Comment.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    lookup_field='pk'
    
    
    
    
        
    