#Grocery Store Checkout Management System

import os
from models import Store

# -----------------------------------------
# Store Tests
# -----------------------------------------

# store1=Store(storeFile="tests/store1.json") #Store With Invalid Items
# store2=Store(storeFile="tests/store2.json") #Store With Invalid Specials

# -----------------------------------------
# Cart Tests
# -----------------------------------------

store3=Store(storeFile="tests/store3.json")

# cart1=store3.createCustomerCart()
# cart1.processItems(cartFile="tests/cart1.json") # ADD action, StaticSpecial
# cart1.getSubtotal()

cart2=store3.createCustomerCart()
cart2.processItems(cartFile="tests/cart2.json") # DynamicSpecial testing
cart2.getSubtotal()

# cart3=store3.createCustomerCart()
# cart3.processItems(cartFile="tests/cart3.json") # ADD + REMOVE actions
# cart3.getSubtotal()

# cart4=store3.createCustomerCart()
# cart4.processItems(cartFile="tests/cart4.json") # REMOVE negative test
# cart4.getSubtotal()

# -----------------------------------------
# Adding Items to customer cart one by one
# -----------------------------------------

# store4=Store(storeFile="tests/store4.json")
# mycart=store4.createCustomerCart()
# mycart.processItem({
#     "item":"Ground beef",
#     "qt":3, 
#     "action":"ADD"
# })
# mycart.processItem({
#     "item":"yogurt",
#     "qt":8,
#     "action":"ADD"
# })
# mycart.processItem({
#     "item":"yogurt",
#     "qt":2,
#     "action":"REMOVE"
# })
# mycart.getSubtotal()

