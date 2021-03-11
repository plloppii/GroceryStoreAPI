
from collections import defaultdict
import json, uuid

#Store Item that is created during the creation process
class StoreItem():
    def __init__(self, name, cost, unit, markdown):
        self.name=name
        self.cost=cost
        self.unit=unit
        self.markdown=markdown
    def __str__(self):
        rtn="{} @ {}/{} ".format(self.name, self.cost, self.unit)
        rtn+=" markdown: {:.2f}".format(self.markdown) if self.markdown and self.markdown>0 else ""
        return rtn

#Two Types of Store Specials
class StoreSpecial():
    pass

class StaticSpecial(StoreSpecial):
    def __init__(self, item:StoreItem, buy:int, cost:int, limit:int=None):
        self.item=item
        self.buy=buy
        self.cost=cost
        self.limit=limit
    def getLineItemDiscount(self, lineItem)->int:
        if lineItem.quantity >= self.buy:
            discountPerSpecialUnit=(lineItem.getCost()*self.buy)-self.cost
            if self.limit: timesApplied=self.limit//self.buy if lineItem.quantity>self.limit else lineItem.quantity//self.buy
            else: timesApplied=lineItem.quantity//self.buy
            return timesApplied*discountPerSpecialUnit
        return 0
    def __str__(self):
        return "{} special: Buy {} for ${}, Limit:{}".format(self.item.name, self.buy, self.cost, self.limit)

class DynamicSpecial(StoreSpecial):
    def __init__(self, item:StoreItem, buy:int, getEqOrLt:int, percentDiscount:int, limit:int=None):
        self.item=item
        self.buy=buy
        self.getEqOrLt=getEqOrLt
        self.percentDiscount=percentDiscount
        self.limit=limit
    def getLineItemDiscount(self, lineItem)->int:
        limit = self.limit // (self.buy + self.getEqOrLt)
        timesApplied= lineItem.quantity // (self.buy + self.getEqOrLt)
        timesApplied= timesApplied if timesApplied < limit else limit
        unitDiscount= lineItem.getCost() * (self.percentDiscount/100)

        discount= timesApplied* (self.getEqOrLt * unitDiscount)
        remaining= lineItem.quantity % (self.buy + self.getEqOrLt) if timesApplied < limit else 0
        discountedRemaining= (remaining-self.buy) * unitDiscount if remaining > self.buy else 0
        return discount+discountedRemaining
    def __str__(self):
        return "{} special: Buy {} get {} equal or less than at {}% off, Limit:{}".format(self.item.name, self.buy, self.getEqOrLt, self.percentDiscount, self.limit)

# Store class that represents the creation of a Store object, containing the store's items and specials.
# holds a hash of customer's carts for fast lookup. 
# Store can be modified with asycronous calls OR at once with a json file. 
class Store():
    def __init__(self, storeFile:str=None):
        # Input of Store Creation
        # json file containing items to be created
        self.items=defaultdict(str)
        self.specials=defaultdict(list)
        self.carts=defaultdict(str)
        if storeFile:
            self.loadStoreFile(storeFile)

    def loadStoreFile(self, storeFile:str):
        with open(storeFile) as f:
            storeConfig=json.load(f)
        self.loadItems(storeConfig.get("items"))
        self.loadSpecials(storeConfig.get("specials"))

    def loadItems(self, itemList:list):
        print()
        print("Loading Items into Store")
        print("------------------------")
        for item in itemList:
            self.loadItem(item)

    def loadItem(self, item:dict):
        name=item.get("name").lower()
        cost=item.get("cost")
        unit=item.get("unit")
        markdown=item.get("markdown")
        if not name or not isinstance(name, str) or \
            not cost or (not isinstance(cost, float) and not isinstance(cost,int)) or cost<=0 or \
                not unit or not isinstance(unit, str) or unit not in ["lb","each"]:
            print("Invalid JSON Item Object. Failed to create Store Item")
            return
        elif markdown and (not (isinstance(markdown, float) or isinstance(markdown, int)) or markdown<0):
            print("Invalid value for markdown attribute")
            return 
        createdItem=StoreItem(
            name=name,
            cost=cost,
            unit=unit,
            markdown=markdown
        )
        print(createdItem)
        self.addItem(createdItem)

    def loadSpecials(self, specialList:list):
        print()
        print("Loading Specials into Store")
        print("---------------------------")
        if specialList:
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
        if "cost" in special:
            cost=special.get("cost")
            limit=special.get("limit") #TODO Type check the json object, 
            if not cost or not isinstance(cost, int):
                print("Invalid value for cost attribute")
                return 
            elif limit and not isinstance(limit, int):
                print("Invalid value for limit attribute")
                return 
            createdStoreSpecial=StaticSpecial(fetchItem,buy,cost,limit)
        #Convert buy N get M X% Off to a Static Special. 
        elif "get" in special:
            get=special.get("get")
            percentDiscount=special.get("percent_discount")
            limit=special.get("limit") 
            if not isinstance(get, int) or \
                (not percentDiscount and (not isinstance(percentDiscount, int) or percentDiscount<=0 or percentDiscount>100)):
                    print("Invalid input for buy... get... for... Special JSON object")
                    return 
            elif limit and not isinstance(limit, int):
                print("Invalid value for limit attribute")
                return 
            cost=(buy*fetchItem.cost)+ ((get*fetchItem.cost) * (percentDiscount/100))

            createdStoreSpecial=StaticSpecial(fetchItem,buy+get,cost,limit)
        elif "get_eq_or_lt" in special:
            getEqOrLt=special.get("get_eq_or_lt")
            percentDiscount=special.get("percent_discount")
            #TODO getEqOrLt+buy should be a multiple of limit if provided. 
            limit=special.get("limit")             
            if not isinstance(getEqOrLt, int) or \
                not percentDiscount or not isinstance(percentDiscount, int):
                print("Invalid input for buy... get_eq_or_lt... percentDiscount... Special JSON object")
                return 
            elif limit and not isinstance(limit, int):
                print("Invalid value for limit attribute")
                return 
            createdStoreSpecial=DynamicSpecial(fetchItem,buy,getEqOrLt,percentDiscount,limit)

        if not createdStoreSpecial:
            print("Input JSON Special object is invalid. Failed to create store special")
            return 
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
            
#LineItem that is stored within the CustomerCart class
#One-One relationship to the StoreItem
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
             
    def __str__(self):
        rtn= "\tQt:{}\t\t{:.2f}".format(self.getQuantity(), self.getSubtotal_NoDiscount())
        if self.discount>0: 
            rtn+= "\nspecial\t\t\t-{:.2f}".format(self.discount)
        return rtn

# CustomerCart's creation is handled by the Store class
# All CustomerCart objects need a store instance
class CustomerCart():
    def __init__(self, storeInstance:Store):
        self.id= str(uuid.uuid4())
        self.store=storeInstance
        self.cart=defaultdict(LineItem)

    def processItems(self, cartFile:str)->None:
        print()
        print("Scanning Items for Cart#{}".format(self.id))
        print("---------------------------")
        with open(cartFile) as f:
            inputCart=json.load(f)
        scanItems=inputCart.get("scannedItems")
         
        for item in scanItems:
            self.processItem(item)

    def processItem(self, item:dict)->None:
        #Return if no Store instance is attached to the object
        if not self.store:
            print("Cart#{} has no Store associated with it!".format(self.id))
            return
        #Parse item and quantity
        itemName=item.get("item").lower()
        itemQt=item.get("qt")
        
        #Fetch the StoreItem from the store.
        fetchItem=self.store.getItem(itemName)
        if not fetchItem:
            print("Scan invalid! {} not found in store".format(itemName))
            return
            
        #Parse Action
        if item.get("action").upper()=="ADD":
            lineItem= self.scanItem(fetchItem, itemQt)
        elif item.get("action").upper()=="REMOVE":
            lineItem= self.removeItem(fetchItem, itemQt)

        #Recalculate Special if lineitem and special exists. 
        fetchSpecial=self.store.getSpecial(itemName)
        if lineItem and fetchSpecial:
            lineItem.discount=fetchSpecial[0].getLineItemDiscount(lineItem)
            
    # Remove a certain quantity OR Remove line item entirely
    # Returns None if lineitem removed and LineItem object if not deleted 
    def removeItem(self, fetchItem, itemQt):
        if fetchItem.name in self.cart:
            lineItem=self.cart[fetchItem.name]
            lineItem.quantity-=itemQt
            if lineItem.quantity <= 0 or itemQt == None: 
                print("Removed {}".format(fetchItem.name))
                del self.cart[fetchItem.name]
            else:
                print("Removed {} Qt.{}".format(fetchItem.name, itemQt))
                return lineItem
        else:
            print("Cannot Remove {}. Non-existant in cart".format(fetchItem.name))
        return None
        
    #Processes item and creates LineItem if necessary
    def scanItem(self, fetchItem:StoreItem, itemQt:int)->LineItem:
        if fetchItem.name in self.cart:
            lineItem=self.cart[fetchItem.name]
            lineItem.quantity+=itemQt
        else:
            self.cart[fetchItem.name]= LineItem(item=fetchItem, quantity=itemQt)
            lineItem=self.cart[fetchItem.name]
        print("Scanned {} Qt.{}".format(lineItem.getName(), itemQt))
        return lineItem

    #Prints out a breakdown of the total and returns the subtotal.
    def getSubtotal(self)->int:
        subtotal=sum([ln.getSubtotal() for ln in self.cart.values()])
        print()
        print("Reciept")
        print("--------")
        for lineItem in self.cart.values():
            print(lineItem.item)
            print(lineItem)

        print("-------------------------------")
        print("Subtotal:\t\t{:.2f}".format(subtotal))
        return subtotal
