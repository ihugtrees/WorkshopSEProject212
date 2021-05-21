from flask import (Flask, render_template, request, redirect, session)

# from OnlineStore.src.presentation_layer.utils import *
from OnlineStore.src.communication_layer.publisher import *

app = Flask(__name__)
store = None
app.secret_key = 'ItShouldBeAnythingButSecret'  # you can set any secret key but remember it should be secret


# creating route for login
@app.route('/', methods=['POST', 'GET'])
def web_login():
    if request.method == 'POST':
        if 'user' in session and session['user'] is not None:
            return redirect('/wronglogin')
        username = request.form.get('username')
        password = request.form.get('password')
        if username is not None and password is not None:
            ans = log_in(username, password)
            if ans[0]:
                session['user'] = ans[1]
                return redirect('/dashboard')
            else:
                return redirect('/wronglogin')
    return render_template("login.html")


@app.route('/wronglogin', methods=['POST', 'GET'])
def wronglogin():
    if request.method == 'POST':
        return redirect('/')
    return render_template("wronglogin.html")


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if 'user' in session and session['user'] is not None:
        return render_template("dashboardAdmin.html")
    return '<h1>You are not logged in.</h1>'  # if the user is not in the session


@app.route('/guest_dashboard', methods=['POST', 'GET'])
def guest_dashboard():
    ans = get_into_site()
    if ans[0]:
        session['user'] = ans[1]
        return render_template("dashboardGuest.html")
    else:
        return redirect('/wronglogin')


@app.route('/storesProducts', methods=['POST', 'GET'])
def storesProducts():
    if 'user' in session and session['user'] is not None:
        return render_template("storesProducts.html")
    return '<h1>You are not logged in.</h1>'  # if the user is not in the session


@app.route('/manageCart', methods=['POST', 'GET'])
def manageCart():
    if 'user' in session and session['user'] is not None:
        return render_template("manageCart.html")
    return '<h1>You are not logged in.</h1>'  # if the user is not in the session


@app.route('/manageStore', methods=['POST', 'GET'])
def manageStore():
    if 'user' in session and session['user'] is not None:
        return render_template("manageStore.html")
    return '<h1>You are not logged in.</h1>'  # if the user is not in the session


@app.route('/logout', methods=['POST', 'GET'])
def web_logout():  # TODO fix logout
    log_out(session['user'])
    session['user'] = None
    return render_template("logout.html")


# @app.route('/userloggedin', methods=['POST', 'GET'])
# def userloggedin():
#     if request.method == 'GET':
#         return render_template("userloggedin.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username is not None and password is not None:
            return render_template("signup.html", message=register(username, password)[1])
    return render_template("signup.html")


@app.route('/addstoremanager', methods=['POST', 'GET'])
def addstoremanager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        return render_template("addstoremanager.html",
                               message=assign_store_manager(session["user"], userid, storeid)[1])
    return render_template("addstoremanager.html")


@app.route('/removeStoreManager', methods=['POST', 'GET'])
def removeStoreManager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        return render_template("removeStoreManager.html",
                               message=remove_store_manager(session["user"], userid, storeid)[1])
    return render_template("removeStoreManager.html")


@app.route('/removeStoreOwner', methods=['POST', 'GET'])
def removeStoreOwner():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        return render_template("removeStoreOwner.html", message=remove_store_owner(session["user"], userid, storeid)[1])
    return render_template("removeStoreOwner.html")


@app.route('/editStoreManager', methods=['POST', 'GET'])
def editStoreManager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        permissionUpdate = request.form.get('permissionUpdate')
        return render_template("editStoreManager.html", message=
        edit_store_manager_permissions(session["user"], userid, permissionUpdate, storeid)[1])
    return render_template("editStoreManager.html")


@app.route('/addStoreOwner', methods=['POST', 'GET'])
def addStoreOwner():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        return render_template("addStoreOwner.html", message=assign_store_owner(session["user"], userid, storeid)[1])
    return render_template("addStoreOwner.html")


@app.route('/productInfo', methods=['POST', 'GET'])
def productInfo():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        product = find_product_by_id(productID, storeID)
        if product[0]:
            return render_template("productInfo.html", storeID=storeID, productID=productID, price=product[1].price)
        return render_template("productInfo.html", storeID=storeID, productID=productID, warning=product[1])
    return render_template("productInfo.html")


@app.route('/storeInfo', methods=['POST', 'GET'])
def storeInfo():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        storeInfo = get_store_info(storeID)
        if storeInfo is None:
            return render_template("storeInfo.html", storeID=storeID, warning="Something went wrong...")
        return render_template("storeInfo.html", storeID=storeID, storeInfo=storeInfo)
    return render_template("storeInfo.html")


@app.route('/prodByCategory', methods=['POST', 'GET'])
def prodByCategory():
    if (request.method == 'POST'):
        category = request.form.get('category')
        products = getProductsByFilter(category=category)
        return render_template("prodByCategory.html", category=category, products=products)
    return render_template("prodByCategory.html")


@app.route('/prodByName', methods=['POST', 'GET'])
def prodByName():
    if (request.method == 'POST'):
        name = request.form.get('name')
        products = getProductsByFilter(name=name)
        return render_template("prodByName.html", name=name, products=products)
    return render_template("prodByName.html")


@app.route('/prodByKeyword', methods=['POST', 'GET'])
def prodByKeyword():
    if (request.method == 'POST'):
        key = request.form.get('key')
        products = getProductsByFilter(key=key)
        return render_template("prodByKeyword.html", products=products)
    return render_template("prodByKeyword.html")


@app.route('/prodMultiFilter', methods=['POST', 'GET'])
def prodMultiFilter():
    if (request.method == 'POST'):
        priceRange = request.form.get('priceRange')
        rating = request.form.get('rating')
        category = request.form.get('category')
        storeRating = request.form.get('storeRating')
        products = getProductsByFilter(priceRange=priceRange, rating=rating, category=category, storeRating=storeRating)
        return render_template("prodMultiFilter.html", products=products)
    return render_template("prodMultiFilter.html")


@app.route('/saveCart', methods=['POST', 'GET'])
def saveCart():
    if 'user' not in session or not save_cart(session['user']):
        return render_template("saveCart.html", message="Error occured, you cart wasnt saved")
    else:
        return render_template("saveCart.html", message="Your cart has been saved")


@app.route('/showCart', methods=['POST', 'GET'])
def showCart():
    return render_template("showCart.html", message=get_cart_info(session['user']))


@app.route('/addToCart', methods=['POST', 'GET'])
def addToCart():
    if (request.method == 'POST'):
        productID = request.form.get('productID')
        quantity = request.form.get('quantity')
        try:
            quantity = int(quantity)
        except:
            return render_template("addToCart.html", message="Quantity must be integer")
        if int(quantity) < 1:
            return render_template("addToCart.html", message="Quantity must be positive")
        addToCartOutput = add_product_to_cart(session['user'], productID=productID, quantity=quantity, store_name=None)
        if addToCartOutput:
            return render_template("addToCart.html", message="Item has been added to cart")
        else:
            return render_template("addToCart.html", message="Error")
    return render_template("addToCart.html")


@app.route('/removeFromCart', methods=['POST', 'GET'])
def removeFromCart():
    if (request.method == 'POST'):
        productID = request.form.get('productID')
        quantity = request.form.get('quantity')
        try:
            quantity = int(quantity)
        except:
            return render_template("removeFromCart.html", message="Quantity must be integer")
        if (int(quantity) < 1):
            return render_template("removeFromCart.html", message="Quantity must be positive")
        addToCartOutput = remove_product_from_cart(session["user"], product_id=productID, quantity=quantity,
                                                   store_name=None)
        if (addToCartOutput):
            return render_template("removeFromCart.html", message="Item has been removed from cart")
        if (addToCartOutput):
            return render_template("removeFromCart.html", message="Item has been removed from cart")
        else:
            return render_template("removeFromCart.html", message="Error")
    return render_template("removeFromCart.html")


@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    price = get_cart_info(session['user']).sum
    if (request.method == 'POST'):
        cardNum = request.form.get('cardNum')
        # if(not checkCartAvailability(session['user'])):
        #     return render_template("checkout.html", price=price,message= "Some items are missing")
        # if (not pay(cardNum)):
        #     return render_template("checkout.html", message="Card is not valid")
        # if (not delivery(session['user'])):
        #     return render_template("checkout.html", message="Delivery is not available")
        if purchase(session["user"], payment_info=None, destination=None):
            return render_template("checkout.html", message="Parchase done successfully", price=0)
        else:
            return render_template("checkout.html", message="Error")
    return render_template("checkout.html", price=price)


@app.route('/openStore', methods=['POST', 'GET'])
def openStore():
    if (request.method == 'POST'):
        storeName = request.form.get('storeName')
        # if(not availableStoreName(storeName)):
        #     return render_template("openStore.html",message= "Store name is not valid")
        if (open_store(storeName, session['user'])):
            return render_template("openStore.html", message="New store has been added")
        else:
            return render_template("openStore.html", message="Something went wrong... try again")
    return render_template("openStore.html")


@app.route('/pastPurchases', methods=['POST', 'GET'])
def pastPurchases():
    return render_template("pastPurchases.html", message=get_user_purchases_history(session['user']))


@app.route('/pastStorePurchases', methods=['POST', 'GET'])
def pastStorePurchases():
    if (request.method == 'POST'):
        storeid = request.form.get('storeid')
        return render_template("pastStorePurchases.html", message=get_store_purchase_history(session["user"], storeid))
    return render_template("pastStorePurchases.html")


@app.route('/addNewProduct', methods=['POST', 'GET'])
def addNewProduct():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        productName = request.form.get('productName')
        productPrice = request.form.get('productPrice')
        productAmout = request.form.get('productAmout')
        productCategory = request.form.get('productCategory')
        productDiscountType = request.form.get('productDiscountType')
        productBuyingType = request.form.get('productBuyingType')
        productDescription = request.form.get('productDescription')
        return render_template("addNewProduct.html", message=
        add_new_product_to_store_inventory(user_name=session["user"], product_id=productID, product_name=productName,
                                           price=productPrice, quantity=productAmout, description=productDescription,
                                           store_name=storeID,
                                           category=productCategory, discount_type=productDiscountType,
                                           buying_type=productBuyingType)[1])
    return render_template("addNewProduct.html")


@app.route('/removeProduct', methods=['POST', 'GET'])
def removeProduct():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        return render_template("removeProduct.html",
                               message=remove_product_from_store_inventory(session["user"], productID, storeID)[1])
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
        productDiscountType = request.form.get('productDiscountType')
        productBuyingType = request.form.get('productBuyingType')
        productCategory = request.form.get('productCategory')
        # take care this func is not implemented yet, only edit description
        return render_template("editProduct.html",
                               message=edit_product(session["user"], product_id=productID, product_name=productName,
                                                    price=productPrice, quantity=productAmout,
                                                    description=productDescription,
                                                    store_name=storeID, category=productCategory,
                                                    discount_type=productDiscountType, buying_type=productBuyingType)[
                                   1])
    return render_template("editProduct.html")


@app.route('/purchaseTypes', methods=['POST', 'GET'])
def purchaseTypes():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("purchaseTypes.html", message=get_buying_types(session["user"], storeID)[1])
    return render_template("purchaseTypes.html")


@app.route('/addPurchaseType', methods=['POST', 'GET'])
def addPurchaseType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        return render_template("addPurchaseType.html", message=add_buying_types(session["user"], storeID, details)[1])
    return render_template("addPurchaseType.html")


@app.route('/editPurchaseType', methods=['POST', 'GET'])
def editPurchaseType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        purchaseType = request.form.get('purchaseType')
        details = request.form.get('details')
        return render_template("editPurchaseType.html", message=
        edit_buying_types(session["user"], storeID=storeID, purchaseType=purchaseType, details=details)[1])
    return render_template("editPurchaseType.html")


@app.route('/addDiscountType', methods=['POST', 'GET'])
def addDiscountType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        return render_template("addDiscountType.html", message=add_discount_type(session["user"], storeID, details)[1])
    return render_template("addDiscountType.html")


@app.route('/editDiscountType', methods=['POST', 'GET'])
def editDiscountType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        discountType = request.form.get('discountType')
        details = request.form.get('details')
        return render_template("editDiscountType.html", message=
        edit_discount_type(session["user"], storeID=storeID, discountType=discountType, details=details)[1])
    return render_template("editDiscountType.html")


@app.route('/discountTypes', methods=['POST', 'GET'])
def discountTypes():
    if (request.method == 'POST'):
        return render_template("discountTypes.html", message=request.form.get('storeID')[1])
    return render_template("discountTypes.html")


@app.route('/addPurchasePolicy', methods=['POST', 'GET'])
def addPurchasePolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        return render_template("addPurchasePolicy.html",
                               message=add_buying_policy(session["user"], storeID, details)[1])
    return render_template("addPurchasePolicy.html")


@app.route('/editPurchasePolicy', methods=['POST', 'GET'])
def editPurchasePolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        purchasePolicy = request.form.get('purchaseType')
        details = request.form.get('details')
        return render_template("editPurchasePolicy.html", message=
        edit_buying_policy(session["user"], storeID=storeID, purchasePolicy=purchasePolicy, details=details)[1])
    return render_template("editPurchasePolicy.html")


@app.route('/purchasePolicy', methods=['POST', 'GET'])
def purchasePolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("purchasePolicy.html", message=get_buying_policy(session["user"], storeID)[1])
    return render_template("purchasePolicy.html")


@app.route('/addDiscountPolicy', methods=['POST', 'GET'])
def addDiscountPolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        return render_template("addDiscountPolicy.html",
                               message=add_discount_policy(session["user"], storeID, details)[1])
    return render_template("addDiscountPolicy.html")


@app.route('/editDiscountPolicy', methods=['POST', 'GET'])
def editDiscountPolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        discountPolicy = request.form.get('discountPolicy')
        details = request.form.get('details')
        return render_template("editDiscountPolicy.html", message=
        edit_discount_policy(session["user"], storeID=storeID, discountPolicy=discountPolicy, details=details)[1])
    return render_template("editDiscountPolicy.html")


@app.route('/discountPolicy', methods=['POST', 'GET'])
def discountPolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("discountPolicy.html", message=get_discount_policy(session["user"], storeID)[1])
    return render_template("discountPolicy.html")


@app.route('/getEmployeeDetails', methods=['POST', 'GET'])
def getEmployeeDetails():
    if (request.method == 'POST'):
        storeid = request.form.get('storeid')
        employeeid = request.form.get('employeeid')
        return render_template("getEmployeeDetails.html",
                               message=get_employee_details(session["user"], storeid, employeeid)[1])
    return render_template("getEmployeeDetails.html")


@app.route('/getEmployeePermissions', methods=['POST', 'GET'])
def getEmployeePermissions():
    if (request.method == 'POST'):
        storeid = request.form.get('storeid')
        employeeid = request.form.get('employeeid')
        return render_template("getEmployeePermissions.html",
                               message=get_employee_permissions(session["user"], storeid, employeeid)[1])
    return render_template("getEmployeePermissions.html")


if __name__ == '__main__':
    app.run(debug=False, host="localhost", port=8000, ssl_context=('cert.pem', 'key.pem'))
