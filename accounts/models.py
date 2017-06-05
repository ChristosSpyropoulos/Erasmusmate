# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    CHOICES = (
        ("Don't care", "Don't care"),
        ('Yes', "Yes"),
        ("No", "No")
    )
    TIME_CHOICES = (
        ('UNKNOWN', 'UNKNOWN'),
        ('1 MONTH', '1 MONTH' ),
        ('2 MONTHS', '2 MONTHS'),
        ('3 MONTHS', '3 MONTHS'),
        ('4 MONTHS', '4 MONTHS'),
        ('5 MONTHS ', '5 MONTHS'),
        ('6 MONTHS ', '6 MONTHS')
    )
    NUM_OF_PEOPLE_CHOICES = (
        ("Don't care", "Don't care" ),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6")
    )
    MEN_OR_WOMEN_CHOICES = (
        ("Don't care", "Don't care"),
        ("Men only", "Men only"),
        ("Women only", "Women only")
    )
    RATE_CHOICES = (
        ("Don't care", "Don't care"),
        ("Absolutely", "Absolutely"),
        ("A bit", "A bit"),
        ("Not really", "Not really"),
        ("Absolutely not", "Absolutely not")
    )

    user = models.OneToOneField(User)

    # additionnal content
    description = models.TextField(max_length=500,blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    # criteria
    hardworking = models.CharField(max_length=20, default=RATE_CHOICES[0][0], choices=RATE_CHOICES)
    partying = models.CharField(max_length=20, default=RATE_CHOICES[0][0], choices=RATE_CHOICES)
    traveling = models.CharField(max_length=20, default=RATE_CHOICES[0][0], choices=RATE_CHOICES)

    # restrictions
    price = models.PositiveIntegerField(default=0)
    smoking_permitted = models.CharField(max_length=10, default=CHOICES[0][0], choices=CHOICES)
    same_nationality_roommates = models.CharField(max_length=10, default=CHOICES[0][0], choices=CHOICES)
    time_of_staying_in_flat = models.CharField(max_length=10, default=TIME_CHOICES[0][0], choices=TIME_CHOICES)
    men_or_women_on_room = models.CharField(max_length=10, default=MEN_OR_WOMEN_CHOICES[0][0], choices=MEN_OR_WOMEN_CHOICES)
    num_of_roommates = models.CharField(max_length=10, default=NUM_OF_PEOPLE_CHOICES[0][0], choices=NUM_OF_PEOPLE_CHOICES)

    class Meta:
            abstract = True


class UserProfile(Profile):
    CUISINE_CHOICES = (
        ('GR', 'GREEK' ),
        ('FR', 'FRENCH'),
        ('CHINESE', 'CHINESE'),
        ('INTERNATIONAL', 'INTERNATIONAL')
    )
    GENDER_CHOICES = (
        ('MALE', "MALE"),
        ('FEMALE', "FEMALE")
    )

    # user additionnal content
    age = models.PositiveIntegerField(default=0,blank=True)
    sex = models.CharField(max_length=10, default='', choices=GENDER_CHOICES)
    email = models.EmailField(max_length=50,blank=False)
    phone = models.IntegerField(default=0,blank=True)
    country_of_origin = models.CharField(max_length=20, default='', blank=True)
    country_of_studies = models.CharField(max_length=20, default='', blank=True)
    city_of_studies = models.CharField(max_length=20, default='', blank=True)
    region = models.CharField(max_length=20, default='',blank=True)
    university = models.CharField(max_length=20,default='',blank=True)
    faculty = models.CharField(max_length=30,default='',blank=True)
    prefered_cuisine = models.CharField(max_length=15, default='', choices=CUISINE_CHOICES)

    def __str__(self):
        return "Profile of {0}".format(self.user.username)


def create_profile(sender, **kwargs):
    if kwargs['created']:   # if the user has been crated
        user_profile = UserProfile.objects.create(user=kwargs['instance'])   # then i am gonna create a user profile

post_save.connect(create_profile, sender=User)
