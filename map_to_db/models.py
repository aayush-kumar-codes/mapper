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

    currency = models.CharField(max_length=10, primary_key=True, verbose_name="Currency")
    depo = models.FloatField(null=True, blank=True)
    vol_offset = models.FloatField(null=True, blank=True)
    ftx_feed_ticker = models.CharField(max_length=50, blank=True)
    implied_r = models.FloatField(null=True, blank=True, verbose_name="Implied R")
    spacing = models.FloatField(default=0.04)
    maturity_factor = models.FloatField(default=1)
    rounding = models.FloatField(default=2)

    def save(self, *args, **kwargs) -> None:
        if self.depo:
            self.depo = round(self.depo, 4)
        if self.vol_offset:
            self.vol_offset = round(self.vol_offset, 4)
        
        super(CurrencySettings, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.currency


class OptionsFixingPrice(CurrencySettings):
    class Meta:
        """
            Proxy model inheriting from Currency Settings model.
            It is used to show the Django's default 
            Options Setting change and custom template for Option Fixing Price.
        """
        verbose_name_plural = 'Options Setting'
        proxy = True


@receiver(signal=post_save, sender=User)
def save_notification(sender, created, instance, **kwargs):
    """
        This signal makes the user as admin by default
    """
    if created:
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
