# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Inventory(models.Model):
    description = models.CharField(max_length=150)
    type = models.CharField(max_length=30)

    def quantity(self):
        return InventoryItemList.objects.filter(inventory_id=self).aggregate(Sum('quantity'))

    class Meta:
        db_table = 'tbl_inventory'


class InventoryItemList(models.Model):
    inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    specification = models.CharField(max_length=100)
    quantity = models.IntegerField()
    defected = models.IntegerField(default=0)

    def used(self):
        return UserInventoryMapping.objects.filter(item_id=self, is_accepted=True).aggregate(Sum('item_quantity'))

    def available(self):
        return self.quantity - self.used - self.defected

    class Meta:
        db_table = 'tbl_inventory_item_list'


class UserInventoryMapping(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(InventoryItemList, on_delete=models.CASCADE)
    item_quantity = models.IntegerField()
    is_pending = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_user_inventory_mapping'


