"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from wapp.views import (
    home,
    CityView,
    logout_user,
    LocationView, 
    weather_bycity,
    weather_byuser,
    LoginView,
    RegisterView,
    city_list,
    make_current,
    delete_city
)
urlpatterns = [
	url(r'^$',home,name="home"),
	url(r'^city/$',login_required(CityView.as_view()),name="city"),
    url(r'^city/list$',city_list,name="city_list"),
    url(r'^city/current/(?P<city_id>[0-9]+)$',make_current,name="make_current"),
    url(r'^city/delete/(?P<city_id>[0-9]+)$',delete_city,name="delete_city"),
    url(r'^weather/city/(?P<city>[0-9]+)/(?P<country>[0-9A-Za-z._%+-]*)$',weather_bycity,name="weather_city"),
    url(r'^weather/location/',login_required(LocationView.as_view()),name="weather_loc"),
    url(r'^weather/me',weather_byuser,name="my_weather"),
    url(r'^login$',LoginView.as_view(),name="login"),
    url(r'^logout$',logout_user,name="logout"),
    url(r'^register',RegisterView.as_view(),name="register"),
    url(r'^admin/', include(admin.site.urls)),
]
