from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signin', views.signinForm, name='sigin_form'),
    url(r'^email_activation/(?P<data>.*)', views.activateAccount, name='activate_account'),
    url(r'^add_inventory_item/(?P<data>.*)', views.addInventoryItem),
    url(r'^add_inventory_item/', views.addInventoryItem),
    url(r'^add_inventory', views.addInventory, name='add_inventory'),
    url(r'list_inventory/(?P<data>.*)', views.listPartiularInventory),
    url(r'^list_inventory', views.listInventory, name='list_inventory'),
    url(r'^delete_inventory_item/(?P<data>.*)', views.deleteInventoryItem),
    url(r'^update_inventory_item/(?P<data>.*)', views.updateInventoryItem),
    url(r'^request_inventory/(?P<data>.*)', views.submitInventoryRequest),
    url(r'^assign_inventory_items/(?P<data>.*)', views.asssignInventories),
    url(r'^delete_inventory_requested/(?P<data>.*)', views.deleteInventoriesRequested),
    url(r'^reject_inventory_request/(?P<data>.*)', views.rejectInventoriesRequested),
    # url(r'^update_inventory_requested/(?P<data>.*)', views.updateInventoriesRequested),
    url(r'assigned_inventory', views.showAssignedInventoriesToUser),
    url(r'^user_inventory_mapping', views.userInventoryMapping),
    url(r'^request_inventory', views.requestInventory),
    url(r'^home', views.get_to_home_page, name='home_page'),
    url(r'^login', views.loginForm, name='login_form'),
    url(r'^', views.get_to_home_page, name='home_page')
]
