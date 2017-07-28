from django.conf.urls import url
from . import views

urlpatterns = [
# Home page after the user logs in
    url(r'^$', views.index, name="landing"),
# Handlers for POST routes
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
# Handlers for routes with peramiters
    # url(r'^add-friend/(?P<id>\d+)$', views.addFriend, name='add-friend'),
    # url(r'^remove-friend/(?P<id>\d+)$', views.removeFriend, name='remove-friend'),

# create a default incase someone trys to add random routes to URL
    url(r'^', views.index, name='default'),
]