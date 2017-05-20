# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.forms import RegistrationForm,EditProfileForm,ProfileForm
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash,login, authenticate    #after changing password user , we want to remain logged in
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.db import transaction


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print "Form is validated"
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)    # login after register automatically
            return redirect(reverse('home:home'))
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'accounts/reg_form.html',args)


def view_profile(request, pk=None):  # pk is not Required
    if pk:
        user = get_object_or_404(User, pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)


def view_list_accounts(request):
    query = request.GET.get("q")
    if query:
        queryset_list = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(userprofile__country_of_origin__icontains=query) |
            Q(userprofile__country_of_studies__icontains=query) |
            Q(userprofile__region__icontains=query) |
            Q(userprofile__university__icontains=query) |
            Q(userprofile__faculty__icontains=query) |
            Q(userprofile__description__icontains=query) |
            Q(userprofile__city_of_studies__icontains=query)
        )
    else:
        queryset_list = User.objects.all()

    paginator = Paginator(queryset_list, 3)
    page = request.GET.get('page')
    try:
        queryset_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset_list = paginator.page(paginator.num_pages)

    args = {'users': queryset_list}
    return render(request, 'accounts/list_mates.html', args)


@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect(reverse('accounts:view_profile'))

    else:   # method == 'GET'
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

        args = {'form': form, 'profile_form': profile_form}
        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            # return redirect('/account/profile')
            return redirect(reverse('accounts:view_profile'))
        else:
            # return redirect('/account/change-password')
            return redirect(reverse('accounts:change_password'))

    else:   # method == 'GET'
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)