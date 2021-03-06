
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

from collections import defaultdict

class StoreItem():
    def __init__(self, name, cost, unit, markdown):
        self.name=name
        self.cost=cost
        self.unit=unit
        self.markdown=markdown

class Special():
    def __init__(self, item, buy, discount, limit):
        self.item=item
        self.buy=buy
        self.discount=discount
        self.limit=limit
        
class Store():
    def __init__(self, items:defaultdict=defaultdict(str), specials:defaultdict=defaultdict(list)):
        self.items=items
        self.specials=specials
    def addItem(self, item:StoreItem):
        self.items[item.name]=item
    def removeItem(self, item:str):
        del self.items[item]
    def addSpecial(self, special:Special):
        self.specials[special.item].append(special)
    def removeSpecial(self, special:Special):
        del self.specials[special.item]


