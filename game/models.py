import uuid

from django.db import models


class Game(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    points = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=0,
    )
    user_name = models.CharField(
        blank=False,
        null=False,
        max_length=255,
    )
    correct_words = models.TextField(
        blank=True,
        null=True,
    )

