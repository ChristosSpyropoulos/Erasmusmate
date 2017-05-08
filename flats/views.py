# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flats.forms import (
    CreateFlatForm,
    EditFlatForm,
)

from flats.models import FlatProfile
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


#@login_required     #this is a decorator
def view_list_flats(request):
    args = {'Flats': FlatProfile.objects.all()}
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
        return render(request, 'flats/create_flat.html',args)


#@login_required
@transaction.atomic
def edit_flat(request):
    if request.method == 'POST':
        flat_form = EditFlatForm(request.POST, instance=request.user.flatprofile)
        if flat_form.is_valid():
            flat_form.save()
            return redirect(reverse('flats:view_flat'))

    else:   #method == 'GET'
        flat_form = EditFlatForm(instance=request.user.flatprofile)

        args = {'flat_form': flat_form}
        return render(request, 'flats/edit_flat.html', args)
