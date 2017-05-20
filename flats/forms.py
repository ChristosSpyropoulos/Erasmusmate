from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from models import FlatProfile


class EditFlatForm(forms.ModelForm):
    # it specifies the metadata for the form itself
    class Meta:
        model = FlatProfile
        #specify the fields i want to show on edit profile page
        exclude = ('user','date')



class CreateFlatForm(forms.ModelForm):
    # it specifies the metadata for the form itself
    class Meta:
        model = FlatProfile
        exclude = ('user','date')
