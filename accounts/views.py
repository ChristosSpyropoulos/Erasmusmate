# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.forms import RegistrationForm, EditProfileForm, ProfileForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login, \
    authenticate  # after changing password user , we want to remain logged in
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.conf import settings
from django.db import transaction
import models


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print "Form is validated"
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)  # login after register automatically
            return redirect(reverse('home:home'))
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'accounts/reg_form.html', args)


def view_profile(request, pk=None):  # pk is not Required
    if pk:
        user = get_object_or_404(User, pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)


def get_choices():
    choices = ['']
    for choice in models.Profile.CHOICES:
        choices.append(choice[0])
    return choices


def get_rate_choices():
    choices = ['']
    for choice in models.Profile.RATE_CHOICES:
        choices.append(choice[0])
    return choices


def get_time_choices():
    choices = ['']
    for choice in models.Profile.TIME_CHOICES:
        choices.append(choice[0])
    return choices


def get_num_of_people_choices():
    choices = ['']
    for choice in models.Profile.NUM_OF_PEOPLE_CHOICES:
        choices.append(choice[0])
    return choices


def get_men_or_women_choices():
    choices = ['']
    for choice in models.Profile.MEN_OR_WOMEN_CHOICES:
        choices.append(choice[0])
    return choices


def get_sex_choices():
    choices = ['']
    for choice in models.UserProfile.GENDER_CHOICES:
        choices.append(choice[0])
    return choices


def get_prefered_cuisine():
    choices = ['']
    for choice in models.UserProfile.CUISINE_CHOICES:
        choices.append(choice[0])
    return choices


def view_list_accounts(request):
    # ---append choices to lists---
    choices_list = get_choices()
    rate_choices_list = get_rate_choices()
    time_choices_list = get_time_choices()
    num_of_people_list = get_num_of_people_choices()
    men_or_women_list = get_men_or_women_choices()
    sex_choices_list = get_sex_choices()
    prefered_cuisine_list = get_prefered_cuisine()

    c_hardworking = rate_choices_list
    c_partying = rate_choices_list
    c_traveling = rate_choices_list
    c_smoking_permitted = choices_list
    c_same_nationality_roommates = choices_list
    c_time_of_staying_in_flat = time_choices_list
    c_men_or_women_on_room = men_or_women_list
    c_num_of_roommates = num_of_people_list
    c_sex = sex_choices_list
    c_prefered_cuisine = prefered_cuisine_list

    # ---end append choices to list---
    # ---create queries---
    q_search = request.GET.get("q_search")
    q_hardworking = request.GET.get("q_hardworking")
    q_partying = request.GET.get("q_partying")
    q_traveling = request.GET.get("q_traveling")
    q_price_from = request.GET.get("q_price_from")
    q_price_to = request.GET.get("q_price_to")
    q_smoking_permitted = request.GET.get("q_smoking_permitted")
    q_same_nationality_roommates = request.GET.get("q_same_nationality_roommates")
    q_time_of_staying_in_flat = request.GET.get("q_time_of_staying_in_flat")
    q_men_or_women_on_room = request.GET.get("q_men_or_women_on_room")
    q_num_of_roommates = request.GET.get("q_num_of_roommates")
    q_age_from = request.GET.get("q_age_from")
    q_age_to = request.GET.get("q_age_to")
    q_sex = request.GET.get("q_sex")
    q_email = request.GET.get("q_email")
    q_country_of_origin = request.GET.get("q_country_of_origin")
    q_country_of_studies = request.GET.get("q_country_of_studies")
    q_city_of_studies = request.GET.get("q_city_of_studies")
    q_region = request.GET.get("q_region")
    q_university = request.GET.get("q_university")
    q_faculty = request.GET.get("q_faculty")
    q_prefered_cuisine = request.GET.get("q_prefered_cuisine")
    # ---end queries---
    if q_search:
        queryset_list = User.objects.filter(
            Q(username__icontains=q_search) |
            Q(first_name__icontains=q_search) |
            Q(last_name__icontains=q_search) |
            Q(email__icontains=q_search) |
            Q(userprofile__country_of_origin__icontains=q_search) |
            Q(userprofile__country_of_studies__icontains=q_search) |
            Q(userprofile__region__icontains=q_search) |
            Q(userprofile__university__icontains=q_search) |
            Q(userprofile__faculty__icontains=q_search) |
            Q(userprofile__description__icontains=q_search) |
            Q(userprofile__city_of_studies__icontains=q_search)
        )
    else:
        queryset_list = User.objects.all()

    if q_hardworking:
        queryset_list = queryset_list.filter(Q(userprofile__hardworking__icontains=q_hardworking))
    if q_partying:
        queryset_list = queryset_list.filter(Q(userprofile__partying__icontains=q_partying))
    if q_traveling:
        queryset_list = queryset_list.filter(Q(userprofile__traveling__icontains=q_traveling))
    if q_price_from:
        queryset_list = queryset_list.filter(Q(userprofile__price__gte=q_price_from))
    if q_price_to:
        queryset_list = queryset_list.filter(Q(userprofile__price__lte=q_price_to))
    if q_smoking_permitted:
        queryset_list = queryset_list.filter(Q(userprofile__smoking_permitted__icontains=q_smoking_permitted))
    if q_same_nationality_roommates:
        queryset_list = queryset_list.filter(
            Q(userprofile__same_nationality_roommates__icontains=q_same_nationality_roommates))
    if q_time_of_staying_in_flat:
        queryset_list = queryset_list.filter(
            Q(userprofile__time_of_staying_in_flat__icontains=q_time_of_staying_in_flat))
    if q_men_or_women_on_room:
        queryset_list = queryset_list.filter(Q(userprofile__men_or_women_on_room__icontains=q_men_or_women_on_room))
    if q_num_of_roommates:
        queryset_list = queryset_list.filter(Q(userprofile__num_of_roommates__icontains=q_num_of_roommates))
    if q_age_from:
        queryset_list = queryset_list.filter(Q(userprofile__age__gte=q_age_from))
    if q_age_to:
        queryset_list = queryset_list.filter(Q(userprofile__age__lte=q_age_to))
    if q_sex:
        queryset_list = queryset_list.filter(Q(userprofile__sex__icontains=q_sex))
    if q_email:
        queryset_list = queryset_list.filter(Q(email__icontains=q_email))
    if q_prefered_cuisine:
        queryset_list = queryset_list.filter(Q(userprofile__prefered_cuisine__icontains=q_prefered_cuisine))
    if q_country_of_origin:
        queryset_list = queryset_list.filter(Q(userprofile__country_of_origin__icontains=q_country_of_origin))
    if q_country_of_studies:
        queryset_list = queryset_list.filter(Q(userprofile__country_of_studies__icontains=q_country_of_studies))
    if q_city_of_studies:
        queryset_list = queryset_list.filter(Q(userprofile__city_of_studies__icontains=q_city_of_studies))
    if q_region:
        queryset_list = queryset_list.filter(Q(userprofile__region__icontains=q_region))
    if q_university:
        queryset_list = queryset_list.filter(Q(userprofile__university__icontains=q_university))
    if q_faculty:
        queryset_list = queryset_list.filter(Q(userprofile__faculty__icontains=q_faculty))

    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    try:
        queryset_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset_list = paginator.page(paginator.num_pages)

    args = {
        'users': queryset_list,
        'hardworking': c_hardworking,
        'partying': c_partying,
        'traveling': c_traveling,
        'smoking_permitted': c_smoking_permitted,
        'same_nationality_roommates': c_same_nationality_roommates,
        'time_of_staying_in_flat': c_time_of_staying_in_flat,
        'men_or_women_on_room': c_men_or_women_on_room,
        'num_of_roommates': c_num_of_roommates,
        'sex': c_sex,
        'prefered_cuisine': c_prefered_cuisine
    }
    return render(request, 'accounts/list_mates.html', args)


@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect(reverse('accounts:view_profile'))

    else:  # method == 'GET'
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

        args = {'form': form, 'profile_form': profile_form}
        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            # return redirect('/account/profile')
            return redirect(reverse('accounts:view_profile'))
        else:
            # return redirect('/account/change-password')
            return redirect(reverse('accounts:change_password'))

    else:  # method == 'GET'
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
