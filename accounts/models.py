from django.db import models
from django.contrib.auth.models import User

class UserDetial(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    cycle_length = models.IntegerField(default=28)
    last_men_date = models.DateField(blank=True, null=True)
    next_men_date = models.DateField(blank=True, null=True)
    period_length = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

