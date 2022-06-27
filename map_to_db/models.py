from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class CurrencySettings(models.Model):
    """
        maps objects of JSON file to the database with currency.
    """
    class Meta:
        verbose_name = 'Options Setting'
        verbose_name_plural = 'Options Setting'

    currency = models.CharField(max_length=10, primary_key=True)
    depo = models.FloatField(null=True, blank=True)
    vol_offset = models.FloatField(null=True, blank=True)
    ftx_feed_ticker = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs) -> None:
        if self.depo:
            self.depo = round(self.depo, 4)
        if self.vol_offset:
            self.vol_offset = round(self.vol_offset, 4)
        
        super(CurrencySettings, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.currency


@receiver(signal=post_save, sender=User)
def save_notification(sender, created, instance, **kwargs):
    """
        This signal makes the user as admin by default
    """
    if created:
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
