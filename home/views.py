# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from home.forms import HomeForm
from home.models import Post
from django.contrib.auth.models import User

from accounts.models import UserProfile
from flats.models import FlatProfile


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get (self, request):    # overwrite get method from Class TemplateView
        form = HomeForm()
        posts = Post.objects.all().order_by('-created')[:5]         #show 5 latest posts
        users = User.objects.exclude(id=request.user.id)[:5]        #show 5 newest users

        args = {'form':form, 'posts':posts, 'users': users}
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)      #fill the form with the data received from the post request
        if form.is_valid():
            post = form.save(commit=False) #we have already associated the form with the model, so the data will be stored in the DB
            post.user = request.user
            post.save()

            text = form.cleaned_data['post']    #post is from forms.py
            form = HomeForm()                   #get an empty form
            return redirect('home:home')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)

def view_home(request):
    flats = FlatProfile.objects.all().order_by('-date')[:5]
    users = UserProfile.objects.all().order_by('-date').exclude(id=request.user.id)[:5]

    args = {'flats': flats, 'users': users}
    return render(request, 'home/home_list.html', args)
