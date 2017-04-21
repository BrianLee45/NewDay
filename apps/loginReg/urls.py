from django.conf.urls import url
from . import views

app_name = "loginReg"

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index$', views.index, name='index'),
    url(r'^login$', views.doLogin, name='logMeIn'),
    url(r'^logout$', views.doLogout, name='logout'),
    url(r'^doRegister$', views.doRegister, name='registerMe'),
    url(r'^welcome$', views.showWelcome, name='welcome')
    # url(r'^doDelete$', views.doDelete, name='doDelete')
]
