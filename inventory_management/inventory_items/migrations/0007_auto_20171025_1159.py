# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 11:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_items', '0006_auto_20171025_1157'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userinventorymapping',
            table='tbl_user_inventory_mapping',
        ),
    ]
