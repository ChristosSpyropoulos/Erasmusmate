# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from home.models import Friend
from home.models import Post

# Register your models here.
admin.site.register(Friend)
admin.site.register(Post)
