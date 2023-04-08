from .models import Article, Comment

from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source='owner.name')
    class Meta:
        model=Comment
        fields="__all__"


class ArticleSerializer(serializers.ModelSerializer):
    owner=serializers.HyperlinkedRelatedField(view_name='user-detail',lookup_field='pk',read_only=True)
    comment=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # owner=serializers.HyperlinkedIdentityField(view_name='user-detail')
    class Meta:
        model=Article
        fields=['id','title','content','owner','created_at','updated_at','published','comment']
    
    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        comment=Comment.objects.create()
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate(self, attrs):
        title=attrs['title']
        qs=Article.objects.filter(title__iexact=title)
        if qs.exists():
            raise serializers.ValidationError(f'<{title}> already exists. Please select a different title')
        return attrs
    
    
    