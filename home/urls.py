from django.conf.urls import url
from home.views import HomeView
from . import views


urlpatterns = [
    url(r'^$', HomeView.as_view(),name='home'),   #as_view method is inherited by superclass of TemplateView(called View)
    #url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', HomeView.change_friends,name='change_friends'),

]
