
# Admin Inventory Creation:
# Creation of items in Store
# Support adding items, checking for specials and markdowns
# Support removing scanned item. keep total correct after removal
# Support Per Unit Item
# Support Per lb Item
# Support Markdown, Discount on per-unit cost (.45 off Yogurt)
# Support Special Buy N get M at %X off. Buy 1 get 1 free, Buy 2 get 1 half off
# Support Specials 3 for $5 Limit on Specials
#   ex. buy 2 get 1 free, limit 6. prevent getting a third free item
# Support Buy N get M of equal or lesser value for %X off, 

# Notes:
# Use delaritive approach to creating the store. 
# Checkout items are read in chronologically
# All specials can be simplified into a Requirement(Buy X) and Discount(Get Y)
# They are worded differently as a mean of marketing and psychological manipulation 

class Store():
    def __init__(self, items:list=None, specials:list=None):
        self.items=items
        self.specials=specials

class StoreItem():
    def __init__(self, name, cost, unit, markdown):
        self.name=name
        self.cost=cost
        self.unit=unit
        self.markdown=markdown


class Special():
    def __init__(self, name, requirement, deal, limit):
        self.name=name
        self.requirement=requirement
        self.discount=discount
        self.limit=limit


