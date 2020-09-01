from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation, PostGenerationMethodCall
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")
    password = PostGenerationMethodCall('set_password', 'Paaswork123@')

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
