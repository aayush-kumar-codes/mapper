from django.db import models


class TrofiTokens(models.Model):
    class Meta:
        verbose_name_plural = 'Trofi Tokens'

    id = models.UUIDField(primary_key=True, editable=False)
    token_id = models.CharField(max_length=30, verbose_name='_id', null=True, blank=True)
    symbol = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    apy = models.DecimalField(max_digits=7, decimal_places=3)
    priority = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return self.symbol