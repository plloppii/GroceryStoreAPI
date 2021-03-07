#Grocery Store Checkout Management System

import os
from models import Store

store1=Store(storeFile="tests/store2.json")
cart1=store1.createCustomerCart()
cart1.processItems(cartFile="tests/cart2.json")

cart1.getSubtotal()


