from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.search_form),
    #url(r'^search-form/$', views.search_form),
    url(r'^pagerstats$', views.getData),
]