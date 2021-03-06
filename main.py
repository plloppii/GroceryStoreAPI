'''
Grocery Store Checkout Management System

https://github.com/PillarTechnology/kata-checkout-order-total

'''
import os
from store import Store, StoreItem, Special
# Admin Inventory Creation:
# Creation of items in Store
# Support Per Unit Item
# Support Per lb Item
# Support Markdown, Discount on per-unit cost
# Support Specials 3 for $5 Limit on Specials 
#   ex. buy 2 get 1 free, limit 6. prevent getting a third free item
# Support removing scanned item. keep total correct after removal
# Support Buy N get M of equal or lesser value for %X off, 


firstStore=Store(storeFile="store1.json")

cart=firstStore.createCustomerCart()
cart.processItems(cartFile="cart1.json")

print(cart.getSubtotal())

# Input During Checkout:
["Ground beef", "soup", "lental", "Rice"]
["SCAN", "REMOVED"]

