from rest_framework import serializers
from users.models import User, Profile, FriendRequest


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)
        read_only_fields = ('id', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'groups', 'user_permissions')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        return user


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('id', 'friends_list', 'stars', 'user', 'confirmed_account')


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
        read_only_fields = ('id', 'timestamp', 'status', 'from_user')
        write_only_fields = ('to_user',)

    def create(self, validated_data):
        friend_request = FriendRequest.objects.create(
            # TODO: WHY ADDING FROM USER IS NECESSARY???
            from_user=validated_data['from_user'],
            to_user=validated_data['to_user']
        )
        return friend_request


class FriendResponseSerializer(serializers.Serializer):
    SELECTION = (
        ('accepted', 'accepted'),
        ('declined', 'declined')
    )
    accepted = serializers.ChoiceField(default=None, required=False, choices=SELECTION)

    def create(self, validated_data):
        accepted = validated_data['accepted']
        return accepted

