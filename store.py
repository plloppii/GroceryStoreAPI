
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

from cart import CustomerCart
from collections import defaultdict
import json, uuid

class StoreItem():
    def __init__(self, name, cost, unit, markdown):
        self.name=name
        self.cost=cost
        self.unit=unit
        self.markdown=markdown
    def __str__(self):
        return "{}: {}$/{} Markdown:{}".format(self.name,self.cost,self.unit,self.markdown)

class Special():
    def __init__(self, item:str, buy:int, discount:str, limit:int):
        self.item=item
        self.buy=buy
        self.discount=discount
        self.limit=limit
    def __str__(self):
        return "Buy: {} {} Get: {} off Limit: {}".format(self.buy, self.item, self.discount, self.limit)

        
class Store():
    def __init__(self, storeFile:str):
        # Input of Store Creation
        # json file containing items to be created
        with open("store1.json") as f:
            storeConfig=json.load(f)
        self.items=defaultdict(str)
        self.specials=defaultdict(list)

        self.load_items(storeConfig.get("items"))
        self.load_specials(storeConfig.get("specials"))
        self.carts=defaultdict(str)


    def load_items(self, itemList:list):
        for item in itemList:
            createdItem=StoreItem(
                name=item.get("name").lower(),
                cost=item.get("cost"),
                unit=item.get("unit"),
                markdown=item.get("markdown")
            )
            self.addItem(createdItem)
    def load_specials(self, specialList:list):
        for special in specialList:
            createdSpecial=Special(
                item=special.get("item").lower(),
                buy=special.get("buy"),
                discount=special.get("discount"),
                limit=special.get("limit")
            )
            self.addSpecial(createdSpecial)

    def addItem(self, item:StoreItem):
        self.items[item.name]=item
    def removeItem(self, item:str):
        del self.items[item]
    def addSpecial(self, special:Special):
        self.specials[special.item].append(special)
    def removeSpecial(self, special:Special):
        del self.specials[special.item]


    def getItem(self, item:str):
        return self.items.get(item)
    def getSpecial(self, item:str):
        return self.specials.get(item)

    def createCustomerCart(self):
        newCart= CustomerCart(self)
        self.carts[newCart.id]=newCart
        return newCart
    
    def __str__(self):
        rtn="Items:\n"
        for i in self.items.values():
            rtn+=i.__str__()+"\n"
        rtn+="Specials:\n" 
        for j in self.specials.values():
            rtn+=j[0].__str__()+"\n"
        return rtn
            

