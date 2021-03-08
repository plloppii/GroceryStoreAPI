
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

class StoreSpecial():
    pass
class StaticSpecial(StoreSpecial):
    def __init__(self, item:StoreItem, buy:int, cost:int, limit:int=None):
        self.item=item
        self.buy=buy
        self.cost=cost
        self.limit=limit

    def __str__(self):
        return "{} special: Buy {} for ${}, Limit:{}".format(self.item.name, self.buy, self.cost, self.limit)

class DynamicSpecial(StoreSpecial):
    def __init__(self, item:StoreItem, buy:int, getEqOrLt:int, percentDiscount:int, limit:int=None):
        self.item=item
        self.buy=buy
        self.getEqOrLt=getEqOrLt
        self.percentDiscount=percentDiscount
        self.limit=limit
    def __str__(self):
        return "{} special: Buy {} get {} equal or less than at {}% off, Limit:{}".format(self.item.name, self.buy, self.getEqOrLt, self.percentDiscount, self.limit)
        
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
        print()
        print("Loading Items into Store")
        print("------------------------")
        for item in itemList:
            self.loadItem(item)

    def loadItem(self, item:dict):
        createdItem=StoreItem(
            name=item.get("name").lower(),
            cost=item.get("cost"),
            unit=item.get("unit"),
            markdown=item.get("markdown")
        )
        print(createdItem)
        self.addItem(createdItem)

    def loadSpecials(self, specialList:list):
        print()
        print("Loading Specials into Store")
        print("---------------------------")
        for special in specialList:
            self.loadSpecial(special)
    
    def loadSpecial(self, special:dict):
        itemName=special.get("item").lower()
        fetchItem=self.getItem(itemName)
        if not fetchItem:
            print("Cannot add special for {}! Item does not exist in store".format(itemName))
            return
        buy= special.get("buy")
        if not buy:
            print("Input specials JSON object does not contain buy attribute!")
            return 
        if type(buy) != int:
            print("buy attribute of Input specials JSON is not of type int!")
            return 

        createdStoreSpecial=None
        #TODO Check validity of the Special
        if "cost" in special:
            cost=special.get("cost")
            limit=special.get("limit") #TODO Type check the json object, 
            createdStoreSpecial=StaticSpecial(fetchItem,buy,cost,limit)
        #Convert buy N get M X% Off to a Static Special. 
        elif "get" in special:
            get=special.get("get")
            percentDiscount=special.get("percent_discount")
            cost=(buy*fetchItem.cost)+ ((get*fetchItem.cost) * (percentDiscount/100))
            limit=special.get("limit") 
            createdStoreSpecial=StaticSpecial(fetchItem,buy+get,cost,limit)
        elif "get_eq_or_lt" in special:
            dynamic=True
            getEqOrLt=special.get("get_eq_or_lt")
            percentDiscount=special.get("percent_discount")
            #TODO getEqOrLt+buy should be a multiple of limit if provided. 
            limit=special.get("limit")             
            createdStoreSpecial=DynamicSpecial(fetchItem,buy,getEqOrLt,percentDiscount,limit)

        if not createdStoreSpecial:
            print("Input JSON Special object is invalid. Failed to create store special")
        print(createdStoreSpecial)
        self.addSpecial(createdStoreSpecial)


    def addItem(self, item:StoreItem):
        self.items[item.name]=item
    def deleteItem(self, item:str):
        del self.items[item]
    def addSpecial(self, special:StoreSpecial):
        self.specials[special.item.name].append(special)
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
    def __init__(self, item:StoreItem, quantity:int):
        self.item=item
        self.quantity=quantity
        self.discount=0
        self.appliedSpecial=None
    
    def getName(self): return self.item.name
    def getCost(self): return self.item.cost
    def getUnit(self): return self.item.unit
    def getMarkdown(self): return self.item.markdown
    def getQuantity(self): return self.quantity
    def getSubtotal(self):
        return self.quantity*(self.getCost()-self.getMarkdown()) - self.discount
    def getSubtotal_NoDiscount(self):
        return self.quantity*(self.getCost()-self.getMarkdown())
    def processSpecial(self, special:StoreSpecial):
        if isinstance(special, StaticSpecial):
            if self.quantity >= special.buy:
                discountPerSpecialUnit=(self.getCost()*special.buy)-special.cost
                if special.limit: timesApplied=special.limit/special.buy if (self.quantity//special.buy)>special.limit else self.quantity//special.buy
                else: timesApplied=self.quantity//special.buy
                self.discount=timesApplied*discountPerSpecialUnit
        elif isinstance(special, DynamicSpecial):
            timesApplied= self.quantity // (special.buy + special.getEqOrLt)
            unitDiscount= self.getCost() * (special.percentDiscount/100)

            discount= timesApplied* (special.getEqOrLt * unitDiscount)
            remaining= self.quantity % (special.buy + special.getEqOrLt)
            discountedRemaining= (remaining-special.buy) * unitDiscount if remaining>special.buy else 0
            self.discount= discount+discountedRemaining
             
    def __str__(self):
        rtn= "\tQt:{}\t\t{:.2f}".format(self.getQuantity(), self.getSubtotal_NoDiscount())
        if self.discount>0: 
            rtn+= "\nspecial\t\t\t-{:.2f}".format(self.discount)
        return rtn

class CustomerCart():
    def __init__(self, storeInstance):
        self.id= str(uuid.uuid4())
        self.store=storeInstance
        self.cart=defaultdict(LineItem)

    def processItems(self, cartFile:str):
        print()
        print("Scanning Items for Cart#{}".format(self.id))
        print("---------------------------")
        with open(cartFile) as f:
            inputCart=json.load(f)
        scanItems=inputCart.get("scannedItems")
         
        for item in scanItems:
            itemName=item.get("item").lower()
            itemQt=item.get("qt")

            fetchItem=self.store.getItem(itemName)
            if not fetchItem:
                print("Scan invalid! {} not found in store".format(itemName))
                continue
            
            if item.get("action").upper()=="ADD":
                lineItem= self.scanItem(fetchItem, itemQt)
            elif item.get("action").upper()=="REMOVE":
                lineItem= self.removeItem(fetchItem, itemQt)

            fetchSpecial=self.store.getSpecial(itemName)
            if lineItem and fetchSpecial:
                lineItem.processSpecial(fetchSpecial[0])
            
    
    def removeItem(self, fetchItem, itemQt):
        if fetchItem.name in self.cart:
            lineItem=self.cart[fetchItem.name]
            lineItem.quantity-=itemQt
            if lineItem.quantity <= 0: 
                print("Removed {}".format(fetchItem.name))
                del fetchItem
            else:
                print("Removed {} Qt.{}".format(fetchItem.name, itemQt))
                return lineItem
        else:
            print("Cannot Remove {}. Non-existant in cart".format(fetchItem.name))
        return None
        
    def scanItem(self, fetchItem:StoreItem, itemQt:int):
        if fetchItem.name in self.cart:
            lineItem=self.cart[fetchItem.name]
            lineItem.quantity+=itemQt
        else:
            self.cart[fetchItem.name]= LineItem(item=fetchItem, quantity=itemQt)
            lineItem=self.cart[fetchItem.name]
        print("Scanned {} Qt.{}".format(lineItem.getName(), itemQt))
        return lineItem

    def getSubtotal(self):
        subtotal=sum([ln.getSubtotal() for ln in self.cart.values()])
        print()
        print("Subtotal for Cart#{}".format(self.id))
        print("----------------------------------")
        for lineItem in self.cart.values():
            print(lineItem.item)
            print(lineItem)

        print("-------------------------------")
        print("Subtotal:\t\t{:.2f}".format(subtotal))
        return subtotal
