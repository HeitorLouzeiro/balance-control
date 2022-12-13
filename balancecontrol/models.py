from django.db import models
from django.utils import timezone

# Create your models here.


class Balance(models.Model):
    OPTION = (
        ("P", "Prohibited"),
        ("E", "Exit")
    )
    value = models.FloatField()
    typeoperation = models.CharField(max_length=1, choices=OPTION)
    datecreate = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.value:.2f}'.replace('.', ',')

    def get_value_format(self):
        return f'{self.value:.2f}'.replace('.', ',')

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'
        ordering = ['datecreate']
