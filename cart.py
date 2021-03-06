from collections import defaultdict
import uuid, json

class LineItem():
    def __init__(self, item, quantity:int):
        self.item=item
        self.quantity=quantity

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
                itemName=item.get("item").lower()
                itemQt=item.get("qt")
                self.addLineItem(itemName, itemQt)
    
    def addLineItem(self, itemstr:str, qt:int):
        itemSpecials=self.store.getSpecial(itemstr)
        item=self.store.getItem(itemstr)
        lineItem=LineItem(item=item, quantity=qt)
        self.cart[itemstr]=(lineItem)

    def getSubtotal(self):
        for ln in self.cart.values():
            print("{} qt:{}\t {}".format(ln.item.name, ln.quantity, ln.item.cost))
        return sum([ln.quantity* ln.item.cost for ln in self.cart.values()])


    

            

        








