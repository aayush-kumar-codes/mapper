from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.forms import ValidationError


class Settings(models.Model):
    class Meta:
        verbose_name_plural = 'Settings'

    days = ArrayField(
        models.PositiveIntegerField(blank=True),
        size=8, null=True, blank=True, verbose_name='Funding Days (array)'
    )

    futures_expiry_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='Futures Expiry Code (for implied rate calculation. e.g. 20221230')

    def __str__(self) -> str:
        return "Settings"