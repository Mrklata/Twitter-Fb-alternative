from rest_framework import routers

from users.api import CreateUserView, CreateProfileView, CreateFriendRequestView, CreateFriendResponseView

router = routers.SimpleRouter()
router.register(r'users', CreateUserView, basename='user')
router.register(r'profiles', CreateProfileView, basename='profile')
router.register(r'friend_request', CreateFriendRequestView, basename='friend_request')
router.register(r'friend_response', CreateFriendResponseView, basename='friend_response')
urlpatterns = router.urls
