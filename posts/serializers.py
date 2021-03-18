from rest_framework import serializers

from posts.models import Post


# Post serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'user', 'rates')

        def create(self, validated_data):
            post = Post.objects.create(
                title=validated_data['title'],
                text=validated_data['text']
            )
            return post
