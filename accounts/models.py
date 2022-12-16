from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


class PassawordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    datecreate = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Passaword Reset Token'
        verbose_name_plural = 'Passawords Reset Tokens'
