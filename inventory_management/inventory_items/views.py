# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core import signing

from inventory_items.forms import UserForm, InventoryForm, InventoryItemForm
from inventory_items.utils import sendactivationemail
from inventory_items.models import Inventory, InventoryItemList, UserInventoryMapping, UserInventoryItemMapping
# Create your views here.


def get_to_home_page(request):
    if request.user.is_active:
        return render(request, 'inventory_items/home.html.haml', {'adminstatus': request.user.is_superuser})
    else:
        return redirect('/inventory/login')


def signinForm(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.errors:
            return render(request, 'inventory_management/signin.html.haml',
                    {'submittedform': form, 'form': form}
                )

        elif User.objects.filter(email=form.cleaned_data['email']).count():
            return render(request, 'inventory_management/signin.html.haml',
                    {'error': 'Email already exists'}
                )

        else:
            form = form.cleaned_data
            user = User.objects.create_user(
                username = form['username'],
                email = form['email'],
                password = form['password1']
            )
            user.is_active = False
            user.save()
            sendactivationemail(user.id, user.username, user.email)
            return render(request, 'inventory_items/info.html.haml', {'submittedform': user})
    else:
        form = UserForm()
        return render(request, 'inventory_management/signin.html.haml', {'form': form, 'submittedform': ''})

def loginForm(request):
    if request.user.is_authenticated():
        return render(request, 'inventory_items/home.html.haml', {'adminstatus': request.user.is_superuser})
    elif request.POST:
        form = UserForm(request.POST)
        username = request.POST['username'].encode('ascii','ignore')
        password = request.POST['password1'].encode('ascii','ignore')

        user = authenticate(
            username = username,
            password = password
        )

        if user:
            if user.is_active:
                login(request, user)
                return render(request, 'inventory_items/home.html.haml', {'adminstatus': user.is_superuser})
        else:
            return render(request, 'inventory_management/login.html.haml',
                    {'error': 'Username, password incorrect or Email id not activated yet.'}
                )
    else:
        form = UserForm()
        return render(request, 'inventory_management/login.html.haml', {'form': form, 'submittedform': ''})


def activateAccount(request, data):
    try:
        value = signing.loads(data)
        user_id = int(value['user_info'])
        user = User.objects.get(id=user_id)
        if user.is_active:
            return HttpResponse("Already activated")
        else:
            user.is_active = True
            user.save()
            return redirect('/inventory/home')
    except ObjectDoesNotExist:
        return HttpResponse("Not valid")

def addInventory(request):
    if len(request.POST) == 0:
        form = InventoryForm()
        return render(request, 'inventory_items/add_inventory.html.haml', {'adminstatus': request.user.is_superuser})
    elif request.POST:
        form = InventoryForm(request.POST)
        if form.errors:
            return render(request, 'inventory_items/add_inventory.html.haml', {'adminstatus': request.user.is_superuser, 'submittedform': form} )
        elif Inventory.objects.filter(type=form.cleaned_data['type']).count():
            return render(request, 'inventory_items/add_inventory.html.haml', {'adminstatus': request.user.is_superuser, 'error': 'Inventory type already exists'})
        else:
            form = form.cleaned_data
            inventory = Inventory(
                type=form['type'],
                description=form['description']
            )
            inventory.save()
            return redirect("/inventory/list_inventory")

def listInventory(request):
    list_of_inventory = Inventory.objects.all()
    list_of_inventory_names = []
    for row in list_of_inventory:
        list_of_inventory_names.append(signing.dumps({'inv_type': row.type}))
    inventory_related_data = zip(list_of_inventory, list_of_inventory_names)
    return render(request, 'inventory_items/list_inventory.html.haml', {'adminstatus': request.user.is_superuser, 'list_of_inventory': inventory_related_data})


def listPartiularInventory(request, data):
    value = signing.loads(data)
    item_name = str(value['inv_type'])
    print(data)
    item_id = Inventory.objects.get(type=item_name).id
    list_inventory_items = InventoryItemList.objects.filter(inventory_id=item_id).all()
    list_of_inventory_item_names = []
    for row in list_inventory_items:
        list_of_inventory_item_names.append(signing.dumps({'inv_type_items': row.id}))
    list_inventory_items = zip(list_inventory_items, list_of_inventory_item_names)
    return render(request, 'inventory_items/list_inventory_item.html.haml', {'adminstatus': request.user.is_superuser, 'item_name': item_name, 'item_id': item_id, 'list_of_inventory_items': list_inventory_items, 'encrypted_item_name': data})


def addInventoryItem(request, data=None):
    value = signing.loads(data)
    item_name = str(value['inv_type'])
    item_id = Inventory.objects.get(type=item_name).id
    form = InventoryItemForm(request.POST)
    if len(request.POST):
        if form.errors:
            return render(request, 'inventory_items/add_inventory_item.html.haml', {'adminstatus': request.user.is_superuser, 'submittedform': form, 'item_name': item_name, 'item_id': item_id})
        else:
            form = form.cleaned_data
            inventory_item = InventoryItemList(
                defected=form['defected'],
                specification=form['specification'],
                inventory_id=form['inventory_id'],
                name=form['name'],
                quantity=form['quantity']
            )
            inventory_item.save()
            redirect_url = "/inventory/list_inventory/"+value
            return redirect(redirect_url)
    else:
        return render(request, 'inventory_items/add_inventory_item.html.haml', {'adminstatus': request.user.is_superuser, 'item_name': item_name, 'item_id': item_id})



def updateInventoryItem(request, data):
    value = signing.loads(data)
    item_id = str(value['inv_type_items'])
    inventory_item_info = InventoryItemList.objects.get(id=item_id)
    print(inventory_item_info.inventory_id)
    if len(request.POST) == 0:
        return render(request, 'inventory_items/update_inventory_item.html.haml', {'adminstatus': request.user.is_superuser, 'item_info': inventory_item_info, 'inv_item_id': data})
    else:
        form = InventoryItemForm(request.POST)
        if form.errors:
            return render(request, 'inventory_items/update_inventory_item.html.haml', {'adminstatus': request.user.is_superuser, 'item_info': inventory_item_info, 'submittedform': form})
        else:
            inventory_item = form.cleaned_data
            InventoryItemList.objects.filter(id=item_id).update(**inventory_item)
            inventory_type_info = Inventory.objects.get(id=inventory_item_info.inventory_id.id)
            import ipdb; ipdb.set_trace()
            redirect_url = "/inventory/list_inventory/"+signing.dumps({'inv_type': str(inventory_type_info.type)})
            return redirect(redirect_url)


def deleteInventoryItem(request, data):
    value = signing.loads(data)
    item_id = int(value['inv_type_items'])
    import ipdb; ipdb.set_trace()
    inventory_item = InventoryItemList.objects.get(id=item_id)
    inventory_type_id = inventory_item.inventory_id.id
    inventory_type = Inventory.objects.get(id=inventory_type_id)
    # InventoryItemList.objects.filter(id=item_id).delete()
    redirect_url = "/inventory/list_inventory/"+signing.dumps({'inv_type': str(inventory_type.type)})
    return redirect(redirect_url)


def requestInventory(request, data=None):
    if len(request.POST) == 0:
        list_of_inventory = Inventory.objects.all()
        quantity_of_inventory_type = []
        list_of_inventory_names = []
        for row in list_of_inventory:
            list_of_inventory_names.append(signing.dumps({'inv_type': row.type}))
        for row in list_of_inventory:
            value = row.quantity()['quantity__sum']
            if value is None:
                value = 0
            quantity_of_inventory_type.append(value)
        inventory_related_data = zip(list_of_inventory, list_of_inventory_names,quantity_of_inventory_type)
        return render(request, 'inventory_items/request_inventory.html.haml', {'adminstatus': request.user.is_superuser, 'list_of_inventory': inventory_related_data})


def submitInventoryRequest(request, data=None):
    value = signing.loads(data)
    item_name = str(value['inv_type'])
    inventory_item_detail = Inventory.objects.get(type=item_name)
    if len(request.POST) == 0:
        inventory_item_quantity = inventory_item_detail.quantity()['quantity__sum']
        if inventory_item_quantity is None:
            inventory_item_quantity = 0
        inventory_item_quantity = int(inventory_item_quantity)
        return render(request, 'inventory_items/request_inventory_form.html.haml', {'adminstatus': request.user.is_superuser, 'inventory_item_detail': inventory_item_detail, 'quantity': inventory_item_quantity, 'data': data})
    else:
        user_inventory_mapping = UserInventoryMapping(
        user_id = User.objects.get(id=request.user.id),
        item_quantity_requested=int(request.POST['quantity']),
        item_id= Inventory.objects.get(id=inventory_item_detail.id)
        )
        user_inventory_mapping.save()
        return redirect("/inventory/list_inventory")


def userInventoryMapping(request):
    user_inventory_mapping = UserInventoryMapping.objects.all()
    user_inventory_mapping_list = []
    for row in user_inventory_mapping:
        user_inventory_mapping_list.append(signing.dumps({'user_inv_mapping_id': row.id}))
    user_inventory_mapping_info = zip(user_inventory_mapping, user_inventory_mapping_list)
    return render(request, 'inventory_items/user_inventory_mapping.html.haml', {'adminstatus': request.user.is_superuser, 'user_inventory_mapping_info': user_inventory_mapping_info})


def asssignInventories(request, data=None):
    value = signing.loads(data)
    user_inv_mapping_id = str(value['user_inv_mapping_id'])
    user_inv_mapping = UserInventoryMapping.objects.get(id=user_inv_mapping_id)
    inventory_item_list = InventoryItemList.objects.filter(inventory_id=user_inv_mapping.item_id)
    if len(request.POST) == 0:
        if user_inv_mapping.is_pending == True:
            return render(request, 'inventory_items/assign_inventories.html.haml', {'adminstatus': request.user.is_superuser, 'inventory_item_list': inventory_item_list, 'user_inv_mapping': user_inv_mapping})
        else:
            return redirect('inventory/user_inventory_mapping')
    else:
        list_inventory_item_id = request.POST.getlist('inventory_item_id')
        list_quantities_assigned = request.POST.getlist('quantity_list')
        sum_quantity = 0
        for quantity in list_quantities_assigned:
            sum_quantity += int(quantity)
        if sum_quantity> user_inv_mapping.item_quantity_requested:
           return render(request, 'inventory_items/assign_inventories.html.haml', {'adminstatus': request.user.is_superuser, 'inventory_item_list': inventory_item_list, 'user_inv_mapping': user_inv_mapping, 'errormsg': 'Quantities assigned cannot be greater than quantities requested'})
        else:
            for item_id, quantity in zip(list_inventory_item_id, list_quantities_assigned):
                inventory_item_id = InventoryItemList.objects.get(id=item_id)
                user_inv_item_mapping = UserInventoryItemMapping(
                    inventory_item_mapping_id=user_inv_mapping,
                    inventory_item_id= inventory_item_id,
                    quantity_assigned=int(quantity)
                )
                user_inv_item_mapping.save()
            user_inv_mapping.is_pending = False
            user_inv_mapping.is_accepted = True
            user_inv_mapping.item_quantity_assigned = sum_quantity
            user_inv_mapping.save()
            return redirect('/inventory/user_inventory_mapping')


def rejectInventoriesRequested(request, data=None):
    value = signing.loads(data)
    user_inv_mapping_id = str(value['user_inv_mapping_id'])
    user_inv_mapping = UserInventoryMapping.objects.get(id=user_inv_mapping_id)
    user_inv_mapping.is_accepted = False
    user_inv_mapping.is_pending = False
    user_inv_mapping.save()
    return redirect('/inventory/user_inventory_mapping')


def deleteInventoriesRequested(request, data=None):
    value = signing.loads(data)
    user_inv_mapping_id = str(value['user_inv_mapping_id'])
    user_inv_mapping = UserInventoryMapping.objects.get(id=user_inv_mapping_id)
    user_inv_mapping.delete()
    return redirect('/inventory/user_inventory_mapping')


def showAssignedInventoriesToUser(request):
    user_inv_mapping_accepted = UserInventoryMapping.objects.filter(user_id=request.user.id, is_accepted=True).all()
    user_inv_mapping_accepted_items_list = []
    for row in user_inv_mapping_accepted:
        user_inv_mapping_accepted_items = x = UserInventoryItemMapping.objects.filter(inventory_item_mapping_id=row.id).all()
        user_inv_mapping_accepted_items_list.append(user_inv_mapping_accepted_items)
    assigned_inventory_items_mapping = zip(user_inv_mapping_accepted, user_inv_mapping_accepted_items_list)
    return render(request, 'inventory_items/show_assigned_inventories.html.haml', {'adminstatus': request.user.is_superuser, 'assigned_inventory_items_mapping': assigned_inventory_items_mapping})
    import ipdb; ipdb.set_trace()
