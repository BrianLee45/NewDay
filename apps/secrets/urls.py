from django.conf.urls import url

from . import views

app_name = "secrets"

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^popular$', views.showPopular, name="popular"),
    url(r'^post$', views.doPost, name="post"),
    url(r'^(?P<secret_id>\d+)/delete$', views.doDelete, name="delete"),
    url(r'^(?P<secret_id>\d+)/like$', views.doLike, name="like")
]
