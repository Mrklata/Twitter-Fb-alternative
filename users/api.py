from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response

from users.models import User, Profile, FriendRequest
from users.serializers import UserSerializer, ProfileSerializer, FriendRequestSerializer, FriendResponseSerializer


# User APIEndpoint
class CreateUserView(viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return User.objects.all()


# Profile APIEndpoint
class CreateProfileView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


class CreateFriendRequestView(viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = FriendRequest
    serializer_class = FriendRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer.is_valid(raise_exception=True)
        receiver_profile = Profile.objects.get(user=serializer.validated_data['to_user'])
        friend_requests_from_user = FriendRequest.objects.filter(from_user=user, to_user=serializer.validated_data['to_user']).count()

        if receiver_profile in user_profile.friends_list.all():
            return Response({
                'status': 'Wrong invite',
                'data': 'already in friends list'
            })
        elif friend_requests_from_user == 1:
            return Response({
                'status': 'Wrong invite',
                'data': 'invitation already exist'
            })

        else:
            serializer.save(from_user=user)
            return Response({"status": 'ok', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(from_user=user) | Q(to_user=user))


class CreateFriendResponseView(viewsets.ModelViewSet, mixins.ListModelMixin):
    serializer_class = FriendResponseSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = FriendRequest.objects.all()

    def get_queryset(self):
        user = self.request.user
        response = FriendRequest.objects.filter(to_user=user)
        return response

    def create(self, request, *args, **kwargs):
        # TODO: FIX CREATE TO DISABLE ACCEPTED AND POST FIELD
        invitations_ids_list = FriendRequest.objects.filter(to_user=self.request.user).values_list('id', flat=True)
        return Response({
            'status': 'ok',
            'detail': 'to response invite select pk',
            'invitations ids': f'{list(invitations_ids_list)}'

        })

    @action(
        methods=['POST', 'GET'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_name='response',
        url_path='response'
    )
    def response_friend_request(self, request, pk=None):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data['accepted'])
        print(friend_request.status)
        if serializer.validated_data['accepted'] is None:

            if serializer.validated_data['accepted'] == 'accepted':
                friend_request.status = 'accepted'
                inviter = Profile.objects.get(user=self.request.user)
                receiver = Profile.objects.get(user=friend_request.to_user)

                inviter.friends_list.add(receiver)
                receiver.friends_list.add(inviter)
                friend_request.save()
                data = FriendRequestSerializer(friend_request).data
            if serializer.validated_data['accepted'] == 'declined':
                friend_request.status = 'declined'
                friend_request.save()
                data = FriendRequestSerializer(friend_request).data
        else:
            data = {f'already responded as {friend_request.status}'}

        return Response({'status': 'ok', 'data': data})
