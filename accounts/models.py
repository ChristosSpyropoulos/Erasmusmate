# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    CHOICES = (
        ("Don't care", "Don't care"),
        ('Yes', "Yes"),
        ("No", "No")
    )
    CUISINE_CHOICES = (
        ('GR' , 'GREEK' ),
        ('FR' , 'FRENCH'),
        ('CHINESE', 'CHINESE'),
        ('INTERNATIONAL', 'INTERNATIONAL')
    )
    GENDER_CHOICES = (
        ('MALE', "MALE"),
        ('FEMALE', "FEMALE")
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
        ("Don't care", "Don't care" ),
        ("1", "1"),("2", "2"),("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9")
    )
    MEN_OR_WOMEN_CHOICES = (
        ("Don't care", "Don't care"),
        ("Men only", "Men only"),
        ("Women only", "Women only")
    )
    user = models.OneToOneField(User)
    age = models.IntegerField(default=0,blank=True)
    sex = models.CharField(max_length=10, default='',choices = GENDER_CHOICES)
    email = models.EmailField(max_length=50,blank=False)
    phone = models.IntegerField(default=0,blank=True)
    country_of_origin = models.CharField(max_length=20, default='',blank=True)
    country_of_studies = models.CharField(max_length=20, default='',blank=True)
    city_of_studies = models.CharField(max_length=20, default='',blank=True)
    region = models.CharField(max_length=20, default='',blank=True)
    university = models.CharField(max_length=20,default='',blank=True)
    faculty = models.CharField(max_length=30,default='',blank=True)
    description = models.CharField(max_length=200, default='',blank=True)
    max_price = models.IntegerField(default=0,blank=True)
    smoker = models.CharField(max_length=10, default='', choices = CHOICES)
    same_nationality_roommates = models.CharField(max_length=10, default='', choices = CHOICES)
    prefered_cuisine = models.CharField(max_length=10, default='', choices=CUISINE_CHOICES)
    time_of_staying_in_flat = models.CharField(max_length=10, default='', choices=TIME_CHOICES)
    num_of_people_on_room = models.CharField(max_length=10, default='', choices = NUM_OF_PEOPLE_CHOICES)
    men_or_women_on_room = models.CharField(max_length=10, default='', choices = MEN_OR_WOMEN_CHOICES )
    image = models.ImageField(upload_to='profile_image', blank=True, default='')

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:   #if the user has been crated
        user_profile = UserProfile.objects.create(user=kwargs['instance'])   #then i am gonna create a user profile

post_save.connect(create_profile, sender=User)

# i dont know if we need this
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
    #instance.userprofile.save()
