from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)
from django.urls import reverse


# Custom user manager
class UserManager(BaseUserManager):
    # Create normal user
    def create_user(self, email, username, first_name, last_name, password=None, is_staff=False, is_superuser=False,
                    active=True):
        if not email and username and first_name and last_name:
            raise ValueError('User must have: username, email, first abd last name')
        if not password:
            raise ValueError('User must have password')

        user_obj = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.active = active
        user_obj.save(using=self.db)

        current_user = Profile.objects.create(user=user_obj)
        current_user.friends_list.add(Profile.objects.get(user=user_obj))
        current_user.save(using=self.db)

        return user_obj

    # Create staffuser
    def create_staffuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password,
            is_staff=True
        )
        return user

    # Create superuser
    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password,
            is_staff=True,
            is_superuser=True
        )

        return user


# Custom user model
class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(unique=True, max_length=225)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff_user(self):
        return self.is_staff

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def is_active_user(self):
        return self.is_active

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={"pk": self.id})

    
# Profile model - base user extension
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmed_account = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    friends_list = models.ManyToManyField('Profile', blank=True)
    stars = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.user.username} Profile'


# Friend request model
class FriendRequest(models.Model):
    STATUS = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('declined', 'declined')
    )

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, default='pending', max_length=50)

    class Meta:
        verbose_name = 'Friend request'
        verbose_name_plural = 'Friend requests'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'Friend request from {self.from_user}, to {self.to_user}'


