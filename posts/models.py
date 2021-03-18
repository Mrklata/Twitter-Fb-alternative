from django.db import models


# Post main model
from users.models import User


class Post(models.Model):
    RATES_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    rates = models.IntegerField(choices=RATES_CHOICES)