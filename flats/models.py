# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class FlatProfile(Profile):
    CHOICES = (
        ("Don't care", "Don't care"),
        ('Yes', "Yes"),
        ("No", "No")
    )
    NUM_OF_PEOPLE_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6")
    )
    PLACE_CHOICES = (
        ('AGH', 'NEAR AGH'),
        ('KAZIMIERZ', 'IN KAZIMIERZ'),
        ('OLD TOWN', 'IN STARE MIASTO'),
    )

    # flat additionnal content
    name = models.CharField(max_length=50, blank=False)
    place = models.CharField(max_length=15, choices=PLACE_CHOICES, blank=False)
    adress = models.CharField(max_length=50, blank=True)
    num_of_room_available = models.CharField(max_length=10, choices=NUM_OF_PEOPLE_CHOICES, blank=False)
    couples_accepted = models.CharField(max_length=10, default=CHOICES[0][0], choices=CHOICES, blank=True)

    def __str__(self):
        return "Flat of {0}".format(self.user.username)
