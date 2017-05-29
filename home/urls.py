from django.conf.urls import url
from home.views import HomeView
from . import views


urlpatterns = [
    url(r'^$', views.view_home, name='home')
]
