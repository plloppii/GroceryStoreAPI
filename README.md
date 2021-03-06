### GroceryStoreAPI

[Requirements](https://github.com/PillarTechnology/kata-checkout-order-total)
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

Notes:
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

## Design
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


# Usage:
python3 main.py


# Requirements
python>=3.0