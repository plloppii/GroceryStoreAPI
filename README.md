### GroceryStoreAPI 
A simple API that emulates the backend of a grocery store.
Admins have the ability to create a store, adding inventory and specials/discounts
Customers checkout by scanning items creating a shopping cart with a specific ID. Specials/discounts are automatically applied
Details such as the pre-tax subtotal of the cart can be fetched.

# Usage:
```
git clone https://github.com/plloppii/GroceryStoreAPI.git
cd GroceryStoreAPI
# Print out usage
python3 main.py
# Run all tests
python3 main.py alltests
```
Run main.py for all tests. Edit and comment out blocks of main.py to view test cases one by one. 

# API Usage:
```
from models import Store
# Store creation
myStore = Store(storeFile="./testStore.json")
# Customer Cart creation
firstCustomerCart = myStore.createCustomerCart()
firstCustomerCart.processItems(cartFile="./myCart.json")
firstCustomerCart.getSubtotal()
```

# Requirements
python>=3.0

[Design Requirements](https://github.com/PillarTechnology/kata-checkout-order-total)
## Admin Inventory Creation
Creation of items in Store
Support Per Unit Item
Support Per lb Item
Support removing scanned item. keep total correct after removal

Support Specials
* Markdown, Discount on per-unit cost
* Buy N for $5 Limit on Specials 
    * ex. buy 2 get 1 free, limit 6. prevent getting a third free item
* Buy N get M of equal or lesser value for %X off, 
    * ex. buy 2 lbs of ground beed, get 1 lb half off

## Notes
Use delaritive approach to creating the store. 
Checkout items are read in chronologically

Specials can be broken down into two categories:

Static Specials can be deducted into a Requirement(Buy X) and Discount(Get Y). 
After the requirement is met, a discount is applied. The limit being how many times the special can be used.

They are sometimes worded differently as a mean of marketing and psychological manipulation 
Ex. The following are all the same Specials:

* Buy 1 Bags of Chips and Get 1 Free, Limit 3 ==> Scan 1 Bag: $2, Next bag scanned: $0
* Buy 1 Bag of Chips and Get 1 100% off, Limit 3  ==> Scan 1 Bag: $2, Next bag Scanned: $0
* Buy 2 Bags of Chips for the price of 1, Limit 3 ==> Scan 1 Bag: $2, Next bag scanned: $0

Another Ex. 

* Buy 3 lbs of Ground Beef and Get 2 lbs half off ==> 3lbs for $10
* Buy 2 lbs of Ground Beef and Get the next 1 lb Free ==> 3lbs for $10
* Buy 3 lbs of Ground Beef for $10 ==> 3lbs for $10 

Dynamic Specials are more complex. After the requirement is met, the discount is applied to the next M units, until a limit is hit. 
Ex. 

* Buy 2 lbs of Ground Beef, Get next 3lbs equal or lesser value for 50% off 
    * Scans 4 lbs-> [2lbs * $5] + [(2lbs * $5) * 50%] = $15

## JSON Object Format
Inputs of the systems are JSON format objects for portability and compatibility
The Grocery Store API is broken down into down parts
First, a store creation process, where a store manager can interact with a UI to create Grocery Items

Example JSON Input for Store Creation:
```
{
    items: [
        {
            name: "Item1",
            cost: 1.50,
            unit: "lbs",
            markdown: 0
        }
    ],
    specials: [
        {
            item: "Item1",
            buy: 3,
            discount: "$1"
        }
    ]
}
```
Example JSON Input of Scanned Checkout:
```
{
    "scannedItems": [
        {
            "item": "ground bEEf",
            "qt": 6,
            "action": "ADD"
        },
        {
            "item": "yogURT",
            "qt": 1,
            "action": "ADD"
        }
    ]
}
```
Specials JSON Object Format:
```
{
    "item": "Item1" [str, required],
    "buy": 2 [int, required],
    "cost": 6 [int, required],
    "limit": 100 [int, optional]
},
{
    "item": "Item2" [str, required],
    "buy": 3 [int, required],
    "get": 2 [int, required],
    "percent_discount": 50 [0<int<100, required]
},
{
    "item": "Granola" [str, required],
    "buy": 3 [int, required],
    "get_eq_or_lt": 2 [int, required],
    "percent_discount": 50 [int, required],
    "limit": 10 [int, optional]
}
```
