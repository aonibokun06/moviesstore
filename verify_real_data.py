#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviesstore.settings')
django.setup()

from popularity.models import MoviePopularity, Region
from cart.models import Order, Item
from accounts.models import UserProfile

print('=== REAL DATA VERIFICATION ===')
print(f'Total Orders in Database: {Order.objects.count()}')
print(f'Total Order Items: {Item.objects.count()}')
print(f'Users with Regions: {UserProfile.objects.count()}')

print('\n=== ORDERS DETAIL ===')
for order in Order.objects.all():
    print(f'Order {order.id}: User {order.user.username}, Total: ${order.total}, Date: {order.date}')
    items = Item.objects.filter(order=order)
    for item in items:
        print(f'  - {item.movie.name}: {item.quantity} units @ ${item.price}')

print('\n=== USER REGIONS ===')
for profile in UserProfile.objects.all():
    print(f'User {profile.user.username}: {profile.region}')

print('\n=== CURRENT POPULARITY DATA ===')
for popularity in MoviePopularity.objects.all():
    print(f'{popularity.movie.name} in {popularity.region.name}: {popularity.purchase_count} purchases, {popularity.view_count} views')

print('\n=== VERIFICATION COMPLETE ===')
