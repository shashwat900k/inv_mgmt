# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import UserForm, InventoryForm, InventoryItemForm
from utils import sendactivationemail
from models import Inventory
from django.shortcuts import redirect
# Create your views here.

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


def activateAccount(request, user_id):
    if User.objects.filter(id=user_id).count():
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return render(request, 'inventory_items/home.html.haml')

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
    for row in list_of_inventory:
        print(row.type)
    return render(request, 'inventory_items/list_inventory.html.haml', {'adminstatus': request.user.is_superuser, 'list_of_inventory': list_of_inventory})
