# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q

from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
    ProfileForm,
)
from accounts.models import UserProfile
from django.shortcuts import (
    render,
    HttpResponse,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash,login, authenticate    #after changing password user , we want to remain logged in
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.db import transaction


#def home(request):
    #numbers =[1,2,3,4,5]
    #name = "George Tsik"

    #args = {'myName': name, 'numbers': numbers}

    #return render(request, 'accounts/home.html',args)



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print "Form is validated"
            #form.save()
            user = form.save()
            #user.refresh_from_db()
            #user.userprofile.city_of_studies = form.cleaned_data.get('city')
            #user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)    #login after register automatically
            return redirect(reverse('home:home'))
        #else:
            #print formset.errors

    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html',args)

#@login_required     #this is a decorator
def view_profile(request, pk=None): #pk is not Required
    if pk:
        user = get_object_or_404(User, pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html',args)

#@login_required     #this is a decorator
def view_list_accounts(request):
    queryset_list = User.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query) |
            Q(country_of_origin__icontains=query) |
            Q(country_of_studies__icontains=query) |
            Q(region__icontains=query) |
            Q(university__icontains=query) |
            Q(faculty__icontains=query) |
            Q(description__icontains=query) |
            Q(city_of_studies__icontains=query)
        )
    args = {'users': queryset_list}
    return render(request, 'accounts/list_mates.html', args)

#@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect(reverse('accounts:view_profile'))

    else:   #method == 'GET'
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

        args = {'form': form, 'profile_form': profile_form}
        return render(request, 'accounts/edit_profile.html', args)

#@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save();
            update_session_auth_hash(request, form.user)
            #return redirect('/account/profile')
            return redirect(reverse('accounts:view_profile'))
        else:
            #return redirect('/account/change-password')
            return redirect(reverse('accounts:change_password'))

    else:   #method == 'GET'
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/user_profile.html', {'user':user})
    #mporei na einai {'user':request.user ;h 'user':userprofile}
