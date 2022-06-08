from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class CurrencyModel(models.Model):
    """
        stores currency passed in JSON file.
    """
    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    currency = models.CharField(max_length=10, primary_key=True)

    def __str__(self) -> str:
        return self.currency


class MappingModel(models.Model):
    """
        maps objects of JSON file to the database with currency.
    """
    class Meta:
        verbose_name_plural = "Mapped Data"

    currency = models.ForeignKey(to=CurrencyModel, on_delete=models.CASCADE)
    depo = models.DecimalField(max_digits=11, decimal_places=8, default=0.0, null=True)
    vol_offset = models.DecimalField(max_digits=11, decimal_places=8, default=0.0, null=True)
    FTX_feed_ticker = models.CharField(max_length=50, blank=True)


@receiver(signal=post_save, sender=User)
def save_notification(sender, created, instance, **kwargs):
    """
        This signal makes the user as admin by default
    """
    if created:
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
