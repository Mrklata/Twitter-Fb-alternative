import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import User, Profile, FriendRequest


@pytest.mark.django_db
def test_create_user(user):
    user = user
    users = User.objects.all()
    profiles = Profile.objects.all()
    assert users.count() == 1
    assert profiles.count() == 1
    assert Profile.objects.filter(user=user.id)

    profile = Profile.objects.get(user=user.id)

    assert profile.user == user


@pytest.mark.django_db
def test_create_friend_request(user_client, user):
    user2 = baker.make(User)

    # fake users
    baker.make(User, _quantity=10)

    friend_request = FriendRequest.objects.create(
        from_user=user,
        to_user=user2
    )

    response = user_client.get(reverse('profile-list'))

    assert friend_request
    assert friend_request.to_user == user2
    assert friend_request.from_user == user
    assert FriendRequest.objects.all().count() == 1
    assert friend_request.status == 'pending'
    assert response.status_code == 200


@pytest.mark.django_db
def test_response_to_friend_request(user_client, user):
    user2 = baker.make(User)

    FriendRequest.objects.create(from_user=user2, to_user=user)




