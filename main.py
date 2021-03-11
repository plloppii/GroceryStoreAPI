#Grocery Store Checkout Management System

import os,sys
from models import Store

# -----------------------------------------
# Store Tests
# -----------------------------------------

def storeTest():
    store1=Store(storeFile="tests/store1.json") #Store With Invalid Items
    store2=Store(storeFile="tests/store2.json") #Store With Invalid Specials

# -----------------------------------------
# Cart Tests
# -----------------------------------------

def cartTest1():
    cart1=store3.createCustomerCart()
    cart1.processItems(cartFile="tests/cart1.json") # ADD action, StaticSpecial
    assert(cart1.getSubtotal() == 31.45)
    print("Pass Test1")

def cartTest2():
    cart2=store3.createCustomerCart()
    cart2.processItems(cartFile="tests/cart2.json") # DynamicSpecial testing
    assert(cart2.getSubtotal() == 32.50)
    print("Pass Test2")

def cartTest3():
    cart3=store3.createCustomerCart()
    cart3.processItems(cartFile="tests/cart3.json") # ADD + REMOVE actions
    assert(cart3.getSubtotal() == 118)
    print("Pass Test3")

def cartTest4():
    cart4=store3.createCustomerCart()
    cart4.processItems(cartFile="tests/cart4.json") # REMOVE negative test
    assert(cart4.getSubtotal() == 63)
    print("Pass Test4")

# -----------------------------------------
# Adding Items to customer cart one by one
# -----------------------------------------

def singleItemsTest():
    store4=Store(storeFile="tests/store4.json")
    mycart=store4.createCustomerCart()
    mycart.processItem({
        "item":"Ground beef",
        "qt":3, 
        "action":"ADD"
    })
    mycart.processItem({
        "item":"yogurt",
        "qt":8,
        "action":"ADD"
    })
    mycart.processItem({
        "item":"yogurt",
        "qt":2,
        "action":"REMOVE"
    })
    mycart.getSubtotal()
    assert(mycart.getSubtotal() == 25)
    print("Pass singleItemsTest")

if __name__ == "__main__":
    validargs= ["storeTest", "alltests", "test1", "test2", "test3", "test4", "singleItemsTest"]
    if len(sys.argv) == 2 and sys.argv[1] in validargs:
        testsToRun=set()
        cartTests=False
        if sys.argv[1] == "storeTest":
            testsToRun.add("storeTest")
        elif sys.argv[1] == "singleItemsTest":
            testsToRun.add("singleItemsTest")
        elif sys.argv[1] == "alltests":                
            cartTests=True
            testsToRun.update(["test1", "test2", "test3", "test4"])
        elif sys.argv[1] in ["test1", "test2", "test3", "test4"]:
            cartTests=True                
            testsToRun.add(sys.argv[1])
        
        if "storeTest" in testsToRun:
            storeTest()
        if "singleItemsTest" in testsToRun:
            singleItemsTest()
        if cartTests:
            store3=Store(storeFile="tests/store3.json")
            if "test1" in testsToRun:
                cartTest1() 
            if "test2" in testsToRun:
                cartTest2()
            if "test3" in testsToRun:
                cartTest3()
            if "test4" in testsToRun:
                cartTest4()
    else:
        print("Usage: python main.py [test_to_run]")
        print("\tOptions:")
        print("\t\t[test_to_run] : storeTest, alltests, test1, test2, test3, test4, singleItemsTest")