from django.conf.urls import url
from . import views

urlpatterns = [
# Home page after the user logs in
    url(r'^$', views.index, name="belt"),
    url(r'^add-friend/(?P<id>\d+)$', views.addFriend, name='add-friend'),
    url(r'^remove-friend/(?P<id>\d+)$', views.removeFriend, name='remove-friend'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),

# create a default incase someone trys to add random routes to URL
    # url(r'^', views.index, name='default'),
]