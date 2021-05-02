users = {"hilay":"hilay"}

#logging in
def check_log_in(username,password):
    if(username in users and password == users[username]):
        return True
    return False

#return true for successful sign up
def signupUtil (username,password):
    return True

def addmanager(userid,storeid):
    return True

def editManager(userid,storeid,permissionUpdate):
    return True

def removeManager(userid,storeid):
    return True

def addOwner(userid,storeid):
    return True

def getProductInfo(storeID,productID):
    return "10"

def getStoreInfo(storeID):
    return "info"

#return true if store exist
def storeExist(storeid):
    return True

#return true if user have permissions to add another user as store manager
def userHasPermissions(storeid,user):
    return True

#return true if the user is store manager (for the specific store)
def isStoreManager(storeid,userid):
    return False

#return true id user exist
def userExist(userid):
    return True

#return all prodect that match all the filters
def getProductsByFilter(name=None,priceRange=None,rating=None,category=None,storeRating=None,key=None):
    return "a\nb\nc"

#save user's cart
def saveCartUtil(user):
    return True

def getCartDetails(user):
    return "a b c"

#add product to cart
def addToCartUtil(productID,quantity):
    return True

#get total cart price before checkout
def getTotalPrice(user):
    return 10

def pay(cardNum):
    return True

def checkCartAvailability(user):
    return True

def delivery(user):
    return True

def removeFromCartUtil(productID,quantity):
    return True

#return true if the name is available
def availableStoreName(storeName):
    return True

#open new store
def openStoreUtil (storeName,user):
    return True

def getPastPurchases (user):
    return "dsadsadsa"

def getPastStorePurchases (storeid):
    return "dsadsadsa"

def addNewProductUtil(storeID,productID,productName,productPrice,productAmout,productDescription):
    return True

def removeProductUtil(storeID,productID):
    return True

def editProductUtil(storeID,productID,productName,productPrice,productAmout,productDescription):
    return True

def getPurchaseTypes(storeID):
    return "dsadsadsa"

def addPurchaseTypeUtil(storeID,details):
    return True

def addDiscountTypeUtil(storeID,details):
    return True

def addPurchasePolicyUtil(storeID,details):
    return True

def addDiscountPolicyUtil(storeID,details):
    return True

def editPurchaseTypeUtil(storeID,purchaseType,details):
    return True

def editPurchasePolicyUtil(storeID,purchasePolicy,details):
    return True

def editDiscountPolicyUtil(storeID,discountPolicy,details):
    return True

def editDiscountTypeUtil(storeID,discountType,details):
    return True

def getDiscountTypes(storeID):
    return "dsadsadsa"

def getPurchasePolicy(storeID):
    return "dsadsadsa"

def getDiscountPolicy(storeID):
    return "dsadsadsa"

def getEmployeeDetailsUtil (storeid,employeeid):
    return "dsadsadsa"

def getEmployeePermissionsUtil (storeid,employeeid):
    return "dsadsadsa"