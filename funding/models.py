from django.db import models

class Future(models.Model):
    future = models.CharField(max_length=10, primary_key=True)

    def __str__(self) -> str:
        return self.future

class FundingBase(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    future = models.ForeignKey(to=Future, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    time = models.DateTimeField()

    def __str__(self) -> str:
        return self.future.future

class FundingRecord(FundingBase):
    class Meta:
        verbose_name_plural = 'Funding Record'
        proxy=True


class TrofiTokens(models.Model):
    class Meta:
        verbose_name_plural = 'Trofi Tokens'

    id = models.UUIDField(primary_key=True, editable=False)
    symbol = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    apy = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self) -> str:
        return self.symbol
        