# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class FlatProfile(models.Model):
    CHOICES = (
        ("Don't care", "Don't care"),
        ('Yes', "Yes"),
        ("No", "No")
    )
    PLACE_CHOICES = (
        ('AGH' , 'NEAR AGH' ),
        ('KAZIMIERZ' , 'IN KAZIMIERZ'),
        ('OLD TOWN', 'IN STARE MIASTO'),
    )
    TIME_CHOICES = (
        ('1 MONTH' , '1 MONTH' ),
        ('2 MONTHS' , '2 MONTHS'),
        ('3 MONTHS', '3 MONTHS'),
        ('4 MONTHS', '4 MONTHS'),
        ('5 MONTHS ', '5 MONTHS'),
        ('6 MONTHS ', '6 MONTHS')
    )
    NUM_OF_PEOPLE_CHOICES = (
        ("1", "1"),("2", "2"),("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9")
    )
    MEN_OR_WOMEN_CHOICES = (
        ("Don't care", "Don't care"),
        ("Men only", "Men only"),
        ("Women only", "Women only")
    )
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=True)
    place = models.CharField(max_length=15, choices = PLACE_CHOICES, blank=False)
    adress = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(default=0,blank=False)
    smoker = models.CharField(max_length=10, default=CHOICES[0][0], choices = CHOICES, blank=True)
    same_nationality_roommates = models.CharField(max_length=10, default=CHOICES[0][0], choices = CHOICES, blank=True)
    time_of_staying_in_flat = models.CharField(max_length=10, choices=TIME_CHOICES, blank=False)
    num_of_people_total = models.CharField(max_length=10, choices = NUM_OF_PEOPLE_CHOICES, blank=False)
    num_of_people_available = models.CharField(max_length=10, choices = NUM_OF_PEOPLE_CHOICES, blank=False)
    men_or_women_on_room = models.CharField(max_length=10, default=MEN_OR_WOMEN_CHOICES[0][0], choices = MEN_OR_WOMEN_CHOICES, blank=True)
    couples_accepted = models.CharField(max_length=10, default=CHOICES[0][0], choices = CHOICES, blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)

    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "Flat: {0}".format(self.name)
