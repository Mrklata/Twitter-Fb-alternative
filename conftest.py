from faker import Faker
import pytest

from users.models import User


@pytest.fixture(scope='session')
def fake():
    return Faker()


@pytest.fixture
def user_data(fake):
    return {
        "username": fake.word(),
        "email": fake.email(),
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }


@pytest.fixture
def user(user_data, django_user_model):
    user = User.objects.create_user(**user_data)
    user.set_password(user_data["password"])
    user.save()
    return user


@pytest.fixture
def user_client(client, user_data):
    client.login(username=user_data["username"], password=user_data["password"])
    return client
