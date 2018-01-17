from django.forms import EmailField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Inventory, InventoryItemList

User._meta.get_field('email')._unique = True

class UserForm(UserCreationForm):
    email = EmailField(min_length=6, max_length=60)
    field_order = ['username', 'email', 'password1', 'password2']

    class meta:
        model = User


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['description', 'type']


class InventoryItemForm(ModelForm):
    class Meta:
        model = InventoryItemList
        fields = ['name', 'specification', 'quantity', 'defected', 'inventory_id']
