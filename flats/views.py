# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from flats.forms import CreateFlatForm, EditFlatForm
from flats.models import FlatProfile
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash,login, authenticate    #after changing password user , we want to remain logged in
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.db import transaction


def get_choices():
    choices = ['']
    for choice in FlatProfile.CHOICES:
        choices.append(choice[0])
    return choices


def get_num_of_people():
    choices = ['']
    for choice in FlatProfile.NUM_OF_PEOPLE_CHOICES:
        choices.append(choice[0])
    return choices


def get_place():
    choices = ['']
    for choice in FlatProfile.PLACE_CHOICES:
        choices.append(choice[0])
    return choices


def view_list_flats(request):
    choises_list = get_choices()
    num_of_people_list = get_num_of_people()
    place_list = get_place()

    c_place = place_list
    c_num_of_people = num_of_people_list
    c_couples_accepted = choises_list

    query = request.GET.get("q")
    q_name = request.GET.get("q_name")
    q_place = request.GET.get("q_place")
    q_adress = request.GET.get("q_adress")
    q_num_of_people = request.GET.get("q_num_of_people")
    q_couples_accepted = request.GET.get("q_couples_accepted")

    if query:
        queryset_list = FlatProfile.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(place__icontains=query) |
            Q(adress__icontains=query)
        )
    else:
        queryset_list = FlatProfile.objects.all()

    if q_name:
        queryset_list = queryset_list.filter(Q(name__icontains=q_name))
    if q_place:
        queryset_list = queryset_list.filter(Q(place__icontains=q_place))
    if q_adress:
        queryset_list = queryset_list.filter(Q(place__icontains=q_adress))
    if q_num_of_people:
        queryset_list = queryset_list.filter(Q(num_of_roommates__icontains=q_num_of_people))
    if q_couples_accepted:
        queryset_list = queryset_list.filter(Q(couples_accepted__icontains=q_couples_accepted))

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
    args = {'Flats': queryset_list,
            'place': c_place,
            'num_of_people': c_num_of_people,
            'couples_accepted': c_couples_accepted}
    return render(request, 'flats/list_flats.html', args)


def view_flat(request, id):
    flat = get_object_or_404(FlatProfile, id=id)

    args = {'flat': flat}
    return render(request, 'flats/flat.html', args)


def my_flat(request):
    if not FlatProfile.objects.filter(user__username=request.user.username):
        return redirect(reverse('flats:create_flat'))
    else:
        return redirect(reverse('flats:edit_flat'))


def create_flat(request):
    if request.method == 'POST':
        form = CreateFlatForm(request.POST)
        if form.is_valid():
            print "Form is validated"
            flat = form.save(commit=False)
            flat.user = request.user
            flat.save()

            return redirect(reverse('flats:view_list_flats'))

    else:
        form = CreateFlatForm()

        args = {'form': form}
        return render(request, 'flats/create_flat.html', args)


@transaction.atomic
def edit_flat(request):
    if request.method == 'POST':
        flat_form = EditFlatForm(request.POST, request.FILES, instance=request.user.flatprofile)
        if flat_form.is_valid():
            flat_form.save()
            return redirect(reverse('flats:view_list_flats'))

    else:   # method == 'GET'
        flat_form = EditFlatForm(instance=request.user.flatprofile)

        args = {'flat_form': flat_form}
        return render(request, 'flats/edit_flat.html', args)
