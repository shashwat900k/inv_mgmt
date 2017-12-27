from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signin', views.signinForm, name='sigin_form'),
    url(r'^email_activation/(?P<user_id>[0-9]+)', views.activateAccount, name='activate_account'),
    url(r'^add_inventory', views.addInventory, name='add_inventory'),
    url(r'^list_inventory', views.listInventory, name='list_inventory'),
    url(r'^', views.loginForm, name='login_form')
]
