# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from home.forms import HomeForm
from home.models import Post
from django.contrib.auth.models import User


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get (self,request):    # overwrite get method from Class TemplateView
        form = HomeForm()
        #posts = Post.objects.all()
        posts = Post.objects.all().order_by('-created')
        #users = User.objects.all()
        users = User.objects.exclude(id=request.user.id)

        args = {'form':form, 'posts':posts, 'users': users}
        return render(request, self.template_name, args)

    def post(self,request):
        form = HomeForm(request.POST)#fill the form with the data received from the post request
        if form.is_valid():
            post = form.save(commit=False) #we have already associated the form with the model, so the data will be stored in the DB
            post.user = request.user
            post.save()

            text = form.cleaned_data['post'] #post is from forms.py
            form = HomeForm()#get an empty form
            return redirect('home:home')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)

    def change_friends(request, operation, pk):
        return redirect('home:home')
