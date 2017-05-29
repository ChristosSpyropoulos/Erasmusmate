# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User

from accounts.models import UserProfile
from flats.models import FlatProfile


def view_home(request):
    flats = FlatProfile.objects.all().order_by('-date')[:5]
    users = UserProfile.objects.all().order_by('-date').exclude(id=request.user.id)[:5]

    args = {'flats': flats, 'users': users}
    return render(request, 'home/home_list.html', args)
