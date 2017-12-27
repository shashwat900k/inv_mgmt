# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from inventory_items.models import Inventory, InventoryItemList

# Register your models here.

admin.site.register(Inventory)
admin.site.register(InventoryItemList)
