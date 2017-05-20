from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.view_list_flats, name='view_list_flats'),
    url(r'^flat/(\d+)$', views.view_flat, name='view_flat'),
    url(r'^my-flat/$', views.my_flat, name='my_flat'),
    url(r'^my-flat/create/$', views.create_flat, name='create_flat'),
    url(r'^my-flat/edit/$', views.edit_flat, name='edit_flat'),

]
