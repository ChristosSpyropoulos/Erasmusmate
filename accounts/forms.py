from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    #city_of_studies = forms.CharField(required=False)  #this feature belongs to our model UserProfile

    class Meta:
        model = User
        #all the fields i want in this form
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    #allows the form to save the data to the model
    #commit: save the data to the DB
    def save(self,commit = True):
            user = super(RegistrationForm, self).save(commit=False)     #commit = false : dont save yet to the DB,cause i havent finished
            user.first_name = self.cleaned_data['first_name']    #cleaned_data : so the data are safe to be saved to the DB (security reason)
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()     #that is going to run SQL in the DB

            return user

class EditProfileForm(forms.ModelForm):
    # it specifies the metadata for the form itself
    class Meta:
        model = User
        #specify the fields i want to show on edit profile page
        fields = (
            'first_name',
            'last_name',
            'email',

        )
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'phone',
            'sex',
            'age',

            'country_of_origin',
            'country_of_studies',
            'city_of_studies',
            'region',
            'university',
            'faculty',

            'time_of_staying_in_flat',
            'max_price',

            'smoker',
            'men_or_women_on_room',
            'same_nationality_roommates',
            'num_of_people_on_room',
            'prefered_cuisine',

            'description',
        )
