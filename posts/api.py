from rest_framework import viewsets, mixins, permissions

from posts.models import Post, PostRates
from posts.serializers import PostSerializer


class CreatePostView(viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = Post
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return serializer.save()

