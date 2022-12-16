from datetime import datetime
from secrets import token_hex

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Balance(models.Model):
    OPTION = (
        ("P", "Prohibited"),
        ("E", "Exit")
    )
    value = models.DecimalField(max_digits=19, decimal_places=2)
    typeoperation = models.CharField(max_length=1, choices=OPTION)
    datecreate = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f'{self.value:.2f}'.replace('.', ',')

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'
        ordering = ['-datecreate']

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = datetime.now().strftime('%S') + token_hex(4)
        super(Balance, self).save(*args, **kwargs)
