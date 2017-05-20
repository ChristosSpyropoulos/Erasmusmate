from django import forms
from home.models import Post
# a 'model form' is a form that it is linked(bound) with a model(it knows where to store the data)

class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write a post...',
        }
    ))

    class Meta:
        model = Post    #the model the form is bound with

        fields = ('post',)
