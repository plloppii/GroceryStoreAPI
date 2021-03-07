
from collections import defaultdict
import json, uuid

class StoreItem():
    def __init__(self, name, cost, unit, markdown):
        self.name=name
        self.cost=cost
        self.unit=unit
        self.markdown=markdown
    def __str__(self):
        rtn="{} @ {}/{} ".format(self.name, self.cost, self.unit)
        rtn+="\nmarkdown: {:.2f}".format(self.markdown) if self.markdown and self.markdown>0 else ""
        return rtn
        #return "{}: {}$/{} Markdown:{}".format(self.name,self.cost,self.unit,self.markdown)

class StoreSpecial():
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
        with open(storeFile) as f:
            storeConfig=json.load(f)
        self.items=defaultdict(str)
        self.specials=defaultdict(list)

        self.loadItems(storeConfig.get("items"))
        self.loadSpecials(storeConfig.get("specials"))
        self.carts=defaultdict(str)


    def loadItems(self, itemList:list):
        for item in itemList:
            createdItem=StoreItem(
                name=item.get("name").lower(),
                cost=item.get("cost"),
                unit=item.get("unit"),
                markdown=item.get("markdown")
            )
            self.addItem(createdItem)
    def loadSpecials(self, specialList:list):
        for special in specialList:
            createdStoreSpecial=StoreSpecial(
                item=special.get("item").lower(),
                buy=special.get("buy"),
                discount=special.get("discount"),
                limit=special.get("limit")
            )
            self.addSpecial(createdStoreSpecial)

    def addItem(self, item:StoreItem):
        self.items[item.name]=item
    def deleteItem(self, item:str):
        del self.items[item]
    def addSpecial(self, special:StoreSpecial):
        self.specials[special.item].append(special)
    def deleteSpecial(self, special:StoreSpecial):
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
        rtn+="StoreSpecials:\n" 
        for j in self.specials.values():
            rtn+=j[0].__str__()+"\n"
        return rtn
            
class LineItem():
    def __init__(self, item, quantity:int):
        self.item=item
        self.quantity=quantity
        self.discount=0
    
    def getName(self): return self.item.name
    def getCost(self): return self.item.cost
    def getUnit(self): return self.item.unit
    def getMarkdown(self): return self.item.markdown
    def getQuantity(self): return self.quantity
    def getSubtotal(self):
        return self.quantity*(self.getCost()-self.getMarkdown())
    def processSpecial(self, special):
        pass

class CustomerCart():
    def __init__(self, storeInstance):
        self.id= str(uuid.uuid4())
        self.store=storeInstance
        self.cart=defaultdict(LineItem)

    def processItems(self, cartFile:str):
        with open(cartFile) as f:
            inputCart=json.load(f)
        scanItems=inputCart.get("scannedItems")
         
        for item in scanItems:
            if item.get("action")=="ADD":
                self.scanItem(item)
    
    def scanItem(self, item:dict):
        itemName=item.get("item").lower()
        itemQt=item.get("qt")

        fetchSpecial=self.store.getSpecial(itemName)
        fetchItem=self.store.getItem(itemName)

        if fetchItem:
            lineItem=LineItem(item=fetchItem, quantity=itemQt)
            if fetchSpecial:
                lineItem.processSpecial(fetchSpecial)
        else:
            print("Scan invalid! {} not found in store".format(itemName))
        
        self.cart[itemName]=lineItem

    def getSubtotal(self):
        subtotal=sum([ln.getSubtotal() for ln in self.cart.values()])

        for lineItem in self.cart.values():
            print(lineItem.item)
            print("\tQt:{}\t\t{:.2f}".format(lineItem.getQuantity(), lineItem.getSubtotal()))

        print("-------------------------------")
        print("Subtotal:\t\t{:.2f}".format(subtotal))
        return subtotal

    

            

        








