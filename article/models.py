from django.db import models
from django.contrib.auth import get_user_model
UserModel = get_user_model()

APP_NAME='article'

class Article(models.Model):
    title=models.CharField(max_length=255,blank=False,null=False,unique=True)
    content=models.TextField()
    owner=models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name='owner')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    published=models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    owner=models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    content=models.TextField()
    post=models.ForeignKey(Article, on_delete=models.CASCADE,related_name='comments')
    created_on=models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return 'Comment{} by {}'.format(self.content, self.owner)
        