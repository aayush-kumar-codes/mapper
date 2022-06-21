from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.forms import ValidationError


class Settings(models.Model):
    class Meta:
        verbose_name_plural = 'Settings'

    days = ArrayField(
        models.PositiveIntegerField(blank=True),
        size=8, null=True, blank=True
    )

    def __str__(self) -> str:
        return "Settings"