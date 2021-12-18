from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ..models import Post, PostPoint, Comment


class PostPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPoint
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    post_points = SerializerMethodField("get_post_point")

    class Meta:
        model = Post
        fields = ('id','title','slug',
                  'author','short_description',
                  'publish','created','status',
                  'image','favourite',
                  'post_points')

    def get_post_point(self, instance: Post):
        return PostPointSerializer(instance.post_post_points,
                                   many=True).data


