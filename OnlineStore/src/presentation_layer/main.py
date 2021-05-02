


from flask import (Flask, render_template, request, redirect, session)
from OnlineStore.src.presentation_layer.utils import *

app = Flask(__name__)
store = None
app.secret_key = 'ItShouldBeAnythingButSecret'     #you can set any secret key but remember it should be secret

#dictionary to store information about users)
# user = {"username": "abc", "password": "xyz"}

# creating route for login
@app.route('/', methods=['POST', 'GET'])
def login():
    if (request.method == 'POST'):
        if(session['user']!=None):
            return redirect('/userloggedin')
        username = request.form.get('username')
        password = request.form.get('password')
        if username != None and password != None:
            if check_log_in(username,password):
                session['user'] = username
                return redirect('/dashboard')
            return redirect('/wronglogin')
    return render_template("login.html")

@app.route('/wronglogin', methods=['POST', 'GET'])
def wronglogin():
    if (request.method == 'POST'):
        return redirect('/')
    return render_template("wronglogin.html")

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if('user' in session and session['user'] != None):
        return render_template("dashboard.html")
    return '<h1>You are not logged in.</h1>'  #if the user is not in the session

@app.route('/storesProducts', methods=['POST', 'GET'])
def storesProducts():
    if('user' in session and session['user'] != None):
        return render_template("storesProducts.html")
    return '<h1>You are not logged in.</h1>'  #if the user is not in the session

@app.route('/manageCart', methods=['POST', 'GET'])
def manageCart():
    if('user' in session and session['user'] != None):
        return render_template("manageCart.html")
    return '<h1>You are not logged in.</h1>'  #if the user is not in the session

@app.route('/manageStore', methods=['POST', 'GET'])
def manageStore():
    if('user' in session and session['user'] != None):
        return render_template("manageStore.html")
    return '<h1>You are not logged in.</h1>'  #if the user is not in the session

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['user'] = None
    return render_template("logout.html")

@app.route('/userloggedin', methods=['POST', 'GET'])
def userloggedin():
    if (request.method == 'GET'):
        return render_template("userloggedin.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if (request.method == 'POST'):
        print ("test")
        username = request.form.get('username')
        password = request.form.get('password')
        if username != None and password != None:
            if signupUtil(username,password):
                return render_template("signup.html",message = "New user has been added! :)")
            else:
                return render_template("signup.html",message = "Wrong register, try again")
    return render_template("signup.html")

@app.route('/addstoremanager', methods=['POST', 'GET'])
def addstoremanager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        if (not storeExist(storeid)):
            return render_template("addstoremanager.html",message = "Store Doesnt exist")
        if(not userHasPermissions(storeid,session['user'])):
            return render_template("addstoremanager.html",message = "User doenst have permissions")
        if (not userExist(userid)):
            return render_template("addstoremanager.html", message="User doesnt exist")
        if(isStoreManager(storeid,userid)):
            return render_template("addstoremanager.html", message="User is already store manager")
        if addmanager(userid,storeid):
            return render_template("addstoremanager.html", message="New store menager has been added")
        else:
            return render_template("addstoremanager.html",message = "Something Went Wrong...")
    return render_template("addstoremanager.html")

@app.route('/removeStoreManager', methods=['POST', 'GET'])
def removeStoraManager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        if (not storeExist(storeid)):
            return render_template("removeStoreManager.html",message = "Store Doesnt exist")
        if(not userHasPermissions(storeid,session['user'])):
            return render_template("removeStoreManager.html",message = "User doenst have permissions")
        if (not userExist(userid)):
            return render_template("removeStoreManager.html", message="User doesnt exist")
        if(not isStoreManager(storeid,userid)):
            return render_template("removeStoreManager.html", message="User is not store manager")
        if removeManager(userid,storeid):
            return render_template("removeStoreManager.html", message="store manager has been removed")
        else:
            return render_template("removeStoreManager.html",message = "Something Went Wrong...")
    return render_template("removeStoreManager.html")

@app.route('/editStoreManager', methods=['POST', 'GET'])
def editStoreManager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        permissionUpdate = request.form.get('permissionUpdate')
        if (not storeExist(storeid)):
            return render_template("editStoreManager.html",message = "Store Doesnt exist")
        if(not userHasPermissions(storeid,session['user'])):
            return render_template("editStoreManager.html",message = "User doenst have permissions")
        if (not userExist(userid)):
            return render_template("editStoreManager.html", message="User doesnt exist")
        if(not isStoreManager(storeid,userid)):
            return render_template("editStoreManager.html", message="User is not store manager")
        if editManager(userid,storeid,permissionUpdate):
            return render_template("editStoreManager.html", message="store manager has been updated")
        else:
            return render_template("editStoreManager.html",message = "Something Went Wrong...")
    return render_template("editStoreManager.html")

@app.route('/addStoreOwner', methods=['POST', 'GET'])
def addStoreOwner():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        if (not storeExist(storeid)):
            return render_template("addStoreOwner.html",message = "Store Doesnt exist")
        if(not userHasPermissions(storeid,session['user'])):
            return render_template("addStoreOwner.html",message = "User doenst have permissions")
        if (not userExist(userid)):
            return render_template("addStoreOwner.html", message="User doesnt exist")
        if(isStoreManager(storeid,userid)):
            return render_template("addStoreOwner.html", message="User is already store manager")
        if addOwner(userid,storeid):
            return render_template("addStoreOwner.html", message="New store owner has been added")
        else:
            return render_template("addStoreOwner.html",message = "Something Went Wrong...")
    return render_template("addStoreOwner.html")

@app.route('/productInfo', methods=['POST', 'GET'])
def productInfo():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        price = getProductInfo(storeID,productID)
        if(price == None):
            return render_template("productInfo.html",storeID=storeID,productID=productID,warning="Wrong store or product")
        return render_template("productInfo.html",storeID=storeID,productID=productID,price=price)
    return render_template("productInfo.html")

@app.route('/storeInfo', methods=['POST', 'GET'])
def storeInfo():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        if(not storeExist(storeID)):
            return render_template("storeInfo.html",storeID=storeID,warning="Wrong store ID")
        storeInfo = getStoreInfo(storeID)
        if(storeInfo == None):
            return render_template("storeInfo.html",storeID=storeID,warning="Something went wrong...")
        return render_template("storeInfo.html",storeID=storeID,storeInfo=storeInfo)
    return render_template("storeInfo.html")

@app.route('/prodByCategory', methods=['POST', 'GET'])
def prodByCategory():
    if (request.method == 'POST'):
        category = request.form.get('category')
        products = getProductsByFilter(category=category)
        return render_template("prodByCategory.html",category=category,products=products)
    return render_template("prodByCategory.html")

@app.route('/prodByName', methods=['POST', 'GET'])
def prodByName():
    if (request.method == 'POST'):
        name = request.form.get('name')
        products = getProductsByFilter(name=name)
        return render_template("prodByName.html",name=name,products=products)
    return render_template("prodByName.html")

@app.route('/prodByKeyword', methods=['POST', 'GET'])
def prodByKeyword():
    if (request.method == 'POST'):
        key = request.form.get('key')
        products = getProductsByFilter(key=key)
        return render_template("prodByKeyword.html",products=products)
    return render_template("prodByKeyword.html")

@app.route('/prodMultiFilter', methods=['POST', 'GET'])
def prodMultiFilter():
    if (request.method == 'POST'):
        priceRange = request.form.get('priceRange')
        rating = request.form.get('rating')
        category  = request.form.get('category')
        storeRating = request.form.get('storeRating')
        products = getProductsByFilter(priceRange=priceRange,rating=rating,category=category,storeRating=storeRating)
        return render_template("prodMultiFilter.html",products=products)
    return render_template("prodMultiFilter.html")

@app.route('/saveCart', methods=['POST', 'GET'])
def saveCart():
    if('user' not in session or not saveCartUtil(session['user'])):
        return render_template("saveCart.html", message="Error occured, you cart wasnt saved")
    else:
        return render_template("saveCart.html", message="Your cart has been saved")

@app.route('/showCart', methods=['POST', 'GET'])
def showCart():
    return render_template("showCart.html", message=getCartDetails(session['user']))

@app.route('/addToCart', methods=['POST', 'GET'])
def addToCart():
    if (request.method == 'POST'):
        productID = request.form.get('productID')
        quantity = request.form.get('quantity')
        try :
            quantity = int(quantity)
        except:
            return render_template("addToCart.html", message="Quantity must be integer")
        if (int(quantity) < 1):
            return render_template("addToCart.html", message="Quantity must be positive")
        addToCartOutput = addToCartUtil(productID=productID,quantity=quantity)
        if(addToCartOutput):
            return render_template("addToCart.html",message="Item has been added to cart")
        else:
            return render_template("addToCart.html",message="Error")
    return render_template("addToCart.html")

@app.route('/removeFromCart', methods=['POST', 'GET'])
def removeFromCart():
    if (request.method == 'POST'):
        productID = request.form.get('productID')
        quantity = request.form.get('quantity')
        try :
            quantity = int(quantity)
        except:
            return render_template("removeFromCart.html", message="Quantity must be integer")
        if (int(quantity) < 1):
            return render_template("removeFromCart.html", message="Quantity must be positive")
        addToCartOutput = removeFromCartUtil(productID=productID,quantity=quantity)
        if (addToCartOutput):
            return render_template("removeFromCart.html", message="Item has been removed from cart")
        if(addToCartOutput):
            return render_template("removeFromCart.html",message="Item has been removed from cart")
        else:
            return render_template("removeFromCart.html",message="Error")
    return render_template("removeFromCart.html")

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    price = getTotalPrice(session['user'])
    if (request.method == 'POST'):
        cardNum = request.form.get('cardNum')
        if(not checkCartAvailability(session['user'])):
            return render_template("checkout.html", price=price,message= "Some items are missing")
        if (not pay(cardNum)):
            return render_template("checkout.html", message="Card is not valid")
        if (not delivery(session['user'])):
            return render_template("checkout.html", message="Delivery is not available")
        return render_template("checkout.html",message="Parchase done successfully",price=0)
    return render_template("checkout.html",price=price)

@app.route('/openStore', methods=['POST', 'GET'])
def openStore():
    if (request.method == 'POST'):
        storeName = request.form.get('storeName')
        if(not availableStoreName(storeName)):
            return render_template("openStore.html",message= "Store name is not valid")
        if (openStoreUtil (storeName,session['user'])):
            return render_template("openStore.html", message="New store has been added")
        else:
            return render_template("openStore.html", message="Something went wrong... try again")
    return render_template("openStore.html")

@app.route('/pastPurchases', methods=['POST', 'GET'])
def pastPurchases():
    return render_template("pastPurchases.html",message = getPastPurchases (session['user']))

@app.route('/pastStorePurchases', methods=['POST', 'GET'])
def pastStorePurchases():
    if (request.method == 'POST'):
        storeid = request.form.get('storeid')
        return render_template("pastStorePurchases.html", message=getPastStorePurchases(storeid))
    return render_template("pastStorePurchases.html")

@app.route('/addNewProduct', methods=['POST', 'GET'])
def addNewProduct():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        productName = request.form.get('productName')
        productPrice = request.form.get('productPrice')
        productAmout = request.form.get('productAmout')
        productDescription = request.form.get('productDescription')
        if(not addNewProductUtil(storeID=storeID,productID=productID,productName=productName,productPrice=productPrice,productAmout=productAmout,productDescription=productDescription)):
            return render_template("addNewProduct.html",message= "Something went wrong...")
        else:
            return render_template("addNewProduct.html", message="New product has been added")
    return render_template("addNewProduct.html")

@app.route('/removeProduct', methods=['POST', 'GET'])
def removeProduct():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        if(not removeProductUtil(storeID=storeID,productID=productID)):
            return render_template("removeProduct.html",message= "Something went wrong...")
        else:
            return render_template("removeProduct.html", message="Product has been removed")
    return render_template("removeProduct.html")

@app.route('/editProduct', methods=['POST', 'GET'])
def editProduct():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        productName = request.form.get('productName')
        productPrice = request.form.get('productPrice')
        productAmout = request.form.get('productAmout')
        productDescription = request.form.get('productDescription')
        if(not editProductUtil(storeID=storeID,productID=productID,productName=productName,productPrice=productPrice,productAmout=productAmout,productDescription=productDescription)):
            return render_template("editProduct.html",message= "Something went wrong...")
        else:
            return render_template("editProduct.html", message="Product has been edited")
    return render_template("editProduct.html")

@app.route('/purchaseTypes', methods=['POST', 'GET'])
def purchaseTypes():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("purchaseTypes.html", message=getPurchaseTypes(storeID))
    return render_template("purchaseTypes.html")

@app.route('/addPurchaseType', methods=['POST', 'GET'])
def addPurchaseType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        if(addPurchaseTypeUtil(storeID,details)):
            return render_template("addPurchaseType.html", message="Purchase type has been added successfully")
        else:
            return render_template("addPurchaseType.html", message="Something went wrong...")
    return render_template("addPurchaseType.html")

@app.route('/editPurchaseType', methods=['POST', 'GET'])
def editPurchaseType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        purchaseType = request.form.get('purchaseType')
        details = request.form.get('details')
        if(not editPurchaseTypeUtil(storeID=storeID,purchaseType=purchaseType,details=details)):
            return render_template("editPurchaseType.html",message= "Something went wrong...")
        else:
            return render_template("editPurchaseType.html", message="Purchase Type has been edited")
    return render_template("editPurchaseType.html")

@app.route('/addDiscountType', methods=['POST', 'GET'])
def addDiscountType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        if(addDiscountTypeUtil(storeID,details)):
            return render_template("addDiscountType.html", message="Discount type has been added successfully")
        else:
            return render_template("addDiscountType.html", message="Something went wrong...")
    return render_template("addDiscountType.html")

@app.route('/editDiscountType', methods=['POST', 'GET'])
def editDiscountType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        discountType = request.form.get('discountType')
        details = request.form.get('details')
        if(not editDiscountTypeUtil(storeID=storeID,discountType=discountType,details=details)):
            return render_template("editDiscountType.html",message= "Something went wrong...")
        else:
            return render_template("editDiscountType.html", message="Discnout Type has been edited")
    return render_template("editDiscountType.html")

@app.route('/discountTypes', methods=['POST', 'GET'])
def discountTypes():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("discountTypes.html", message=getDiscountTypes(storeID))
    return render_template("discountTypes.html")

@app.route('/addPurchasePolicy', methods=['POST', 'GET'])
def addPurchasePolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        if(addPurchasePolicyUtil(storeID,details)):
            return render_template("addPurchasePolicy.html", message="Purchase Policy has been added successfully")
        else:
            return render_template("addPurchasePolicy.html", message="Something went wrong...")
    return render_template("addPurchasePolicy.html")

@app.route('/editPurchasePolicy', methods=['POST', 'GET'])
def editPurchasePolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        purchasePolicy = request.form.get('purchaseType')
        details = request.form.get('details')
        if(not editPurchasePolicyUtil(storeID=storeID,purchasePolicy=purchasePolicy,details=details)):
            return render_template("editPurchasePolicy.html",message= "Something went wrong...")
        else:
            return render_template("editPurchasePolicy.html", message="Purchase Policy has been edited")
    return render_template("editPurchasePolicy.html")

@app.route('/purchasePolicy', methods=['POST', 'GET'])
def purchasePolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("purchasePolicy.html", message=getPurchasePolicy(storeID))
    return render_template("purchasePolicy.html")

@app.route('/addDiscountPolicy', methods=['POST', 'GET'])
def addDiscountPolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        if(addDiscountPolicyUtil(storeID,details)):
            return render_template("addDiscountPolicy.html", message="Discount Policy has been added successfully")
        else:
            return render_template("addDiscountPolicy.html", message="Something went wrong...")
    return render_template("addDiscountPolicy.html")

@app.route('/editDiscountPolicy', methods=['POST', 'GET'])
def editDiscountPolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        discountPolicy = request.form.get('discountPolicy')
        details = request.form.get('details')
        if(not editDiscountPolicyUtil(storeID=storeID,discountPolicy=discountPolicy,details=details)):
            return render_template("editDiscountPolicy.html",message= "Something went wrong...")
        else:
            return render_template("editDiscountPolicy.html", message="Discnout Policy has been edited")
    return render_template("editDiscountPolicy.html")

@app.route('/discountPolicy', methods=['POST', 'GET'])
def discountPolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("discountPolicy.html", message=getDiscountPolicy(storeID))
    return render_template("discountPolicy.html")

@app.route('/getEmployeeDetails', methods=['POST', 'GET'])
def getEmployeeDetails():
    if (request.method == 'POST'):
        storeid = request.form.get('storeid')
        employeeid = request.form.get('employeeid')
        return render_template("getEmployeeDetails.html", message=getEmployeeDetailsUtil(storeid,employeeid))
    return render_template("getEmployeeDetails.html")

@app.route('/getEmployeePermissions', methods=['POST', 'GET'])
def getEmployeePermissions():
    if (request.method == 'POST'):
        storeid = request.form.get('storeid')
        employeeid = request.form.get('employeeid')
        return render_template("getEmployeePermissions.html", message=getEmployeePermissionsUtil(storeid,employeeid))
    return render_template("getEmployeePermissions.html")

if __name__ == '__main__':
    # app.run(debug=True,host="localhost",port=8000,ssl_context='adhoc')
    app.run(debug=True,host="localhost",port=8000)