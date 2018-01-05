from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signin', views.signinForm, name='sigin_form'),
    url(r'^email_activation/(?P<data>.*)', views.activateAccount, name='activate_account'),
    url(r'^add_inventory', views.addInventory, name='add_inventory'),
    url(r'^list_inventory', views.listInventory, name='list_inventory'),
    url(r'^home', views.get_to_home_page, name='home_page'),
    url(r'^login', views.loginForm, name='login_form'),
    url(r'^', views.get_to_home_page, name='home_page')
]
