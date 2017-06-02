from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from models import FlatProfile


class EditFlatForm(forms.ModelForm):
    # it specifies the metadata for the form itself
    class Meta:
        model = FlatProfile
        #specify the fields i want to show on edit profile page
        fields = (
            'name',
            'description',
            'place',
            'adress',

            'hardworking',
            'partying',
            'traveling',

            'price',
            'time_of_staying_in_flat',
            'smoking_permitted',
            'men_or_women_on_room',
            'same_nationality_roommates',
            'num_of_roommates',
            'num_of_room_available',
            'couples_accepted',

            'image',
        )



class CreateFlatForm(forms.ModelForm):
    # it specifies the metadata for the form itself
    class Meta:
        model = FlatProfile
        fields = (
            'name',
            'description',
            'place',
            'adress',

            'hardworking',
            'partying',
            'traveling',

            'price',
            'time_of_staying_in_flat',
            'smoking_permitted',
            'men_or_women_on_room',
            'same_nationality_roommates',
            'num_of_roommates',
            'num_of_room_available',
            'couples_accepted',

            'image',
        )
