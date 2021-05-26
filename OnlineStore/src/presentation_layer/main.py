from flask import (Flask, render_template, request, redirect, session)
from flask_socketio import SocketIO, send, join_room

import OnlineStore.src.presentation_layer.utils as utils
from OnlineStore.src.communication_layer import publisher

topics = dict()
app = Flask(__name__)
# store = None
app.secret_key = 'ItShouldBeAnythingButSecret'  # you can set any secret key but remember it should be secret

socketio = SocketIO(app)


# app.config['SECRET_KEY'] = 'secret!'


# dictionary to store information about users)
# user = {"username": "abc", "password": "xyz"}

@socketio.on('join')
def on_join(data):
    join_room(session['username'])

@socketio.on('send messages')
def on_send_messages(data):
    publisher.send_messages(session['username'])

@socketio.on("connect")
def on_connect():
    pass

@socketio.on("close")
def on_close(data):
    print("close")


# creating route for login
@app.route('/', methods=['POST', 'GET'])
def web_login():
    if request.method == 'POST':
        if 'user' in session and session['user'] is not None:
            print("buuuuuug")
            # return redirect('/wronglogin')
        username = request.form.get('username')
        password = request.form.get('password')
        username_hash = utils.log_in(username, password)
        if username_hash[0]:
            resp = redirect('/dashboard')
            resp.set_cookie('username', username_hash[1])
            session['username'] = username
            session['user'] = username_hash[1]
            # print(session['user'])
            return resp
        elif username_hash[1] == "Already loggedIn":
            return redirect('/userloggedin')
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
    if (request.method == 'POST' and 'user' in session and session['user'] is not None and request.form.get('storeID') is not None):
        user = session['user']
        storeID = request.form.get('storeID')
        if(utils.userIsStoreOwner(user,storeID)):
            session["store"] = storeID
            return render_template("manageStoreOwner.html")
        if(utils.userIsStoreManager(user,storeID)):
            session["store"] = storeID
            return render_template("manageStoreManager.html")
        return render_template("signup.html")
    if 'user' in session and session['user'] is not None:
        return render_template("dashboard.html")
    return '<h1>You are not logged in.</h1>'  # if the user is not in the session


@app.route('/guest_dashboard', methods=['POST', 'GET'])
def guest_dashboard():
    ans = utils.get_into_site()
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


@app.route('/manageStoreOwner', methods=['POST', 'GET'])
def manageStoreOwner():
    if 'user' in session and session['user'] is not None:
        return render_template("manageStoreOwner.html")
    return '<h1>You are not logged in.</h1>'  # if the user is not in the session

@app.route('/manageStoreManager', methods=['POST', 'GET'])
def manageStoreManager():
    if 'user' in session and session['user'] is not None:
        return render_template("manageStoreManager.html")
    return '<h1>You are not logged in.</h1>'  # if the user is not in the session


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    utils.log_out(session['user'])
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
        age = request.form.get('age')
        password = request.form.get('password')
        if username is not None and password is not None:
            return render_template("signup.html", message=utils.register(username, password)[1])
    return render_template("signup.html")


@app.route('/addstoremanager', methods=['POST', 'GET'])
def addstoremanager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session["store"]
        return render_template("addstoremanager.html",
                               message=utils.assign_store_manager(session["user"], userid, storeid)[1])
    return render_template("addstoremanager.html")


@app.route('/removeStoreManager', methods=['POST', 'GET'])
def removeStoreManager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session["store"]
        return render_template("removeStoreManager.html",
                               message=utils.remove_store_manager(session["user"], userid, storeid)[1])
    return render_template("removeStoreManager.html")


@app.route('/removeStoreOwner', methods=['POST', 'GET'])
def removeStoreOwner():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session['store']
        return render_template("removeStoreOwner.html", message=utils.remove_store_owner(session["user"], userid, storeid)[1])
    return render_template("removeStoreOwner.html")


@app.route('/editStoreManager', methods=['POST', 'GET'])
def editStoreManager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session["store"]
        permissionUpdate = request.form.get('permissionUpdate')
        return render_template("editStoreManager.html", message=
        utils.edit_store_manager_permissions(session["user"], userid, permissionUpdate, storeid)[1])
    return render_template("editStoreManager.html")


@app.route('/addStoreOwner', methods=['POST', 'GET'])
def addStoreOwner():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = request.form.get('storeid')
        return render_template("addStoreOwner.html", message=utils.assign_store_owner(session["user"], userid, storeid)[1])
    return render_template("addStoreOwner.html")


@app.route('/productInfo', methods=['POST', 'GET'])
def productInfo():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        product = utils.find_product_by_id(productID, storeID)
        if product[0]:
            return render_template("productInfo.html", storeID=storeID, productID=productID, price=product[1].price)
        return render_template("productInfo.html", storeID=storeID, productID=productID, warning=product[1])
    return render_template("productInfo.html")


@app.route('/storeInfo', methods=['POST', 'GET'])
def storeInfo():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        storeInfo = utils.get_store_info(storeID)
        if storeInfo is None:
            return render_template("storeInfo.html", storeID=storeID, warning="Something went wrong...")
        return render_template("storeInfo.html", storeID=storeID, storeInfo=storeInfo)
    return render_template("storeInfo.html")


@app.route('/prodByCategory', methods=['POST', 'GET'])
def prodByCategory():
    if (request.method == 'POST'):
        category = request.form.get('category')
        products = utils.getProductsByFilter(category=category)
        return render_template("prodByCategory.html", category=category, products=products)
    return render_template("prodByCategory.html")


@app.route('/prodByName', methods=['POST', 'GET'])
def prodByName():
    if (request.method == 'POST'):
        name = request.form.get('name')
        products = utils.getProductsByFilter(name=name)
        return render_template("prodByName.html", name=name, products=products)
    return render_template("prodByName.html")


@app.route('/prodByKeyword', methods=['POST', 'GET'])
def prodByKeyword():
    if (request.method == 'POST'):
        key = request.form.get('key')
        products = utils.getProductsByFilter(key=key)
        return render_template("prodByKeyword.html", products=products)
    return render_template("prodByKeyword.html")


@app.route('/prodMultiFilter', methods=['POST', 'GET'])
def prodMultiFilter():
    if (request.method == 'POST'):
        priceRange = request.form.get('priceRange')
        rating = request.form.get('rating')
        category = request.form.get('category')
        storeRating = request.form.get('storeRating')
        products = utils.getProductsByFilter(priceRange=priceRange, rating=rating, category=category, storeRating=storeRating)
        return render_template("prodMultiFilter.html", products=products)
    return render_template("prodMultiFilter.html")


@app.route('/saveCart', methods=['POST', 'GET'])
def saveCart():
    if 'user' not in session or not utils.save_cart(session['user']):
        return render_template("saveCart.html", message="Error occured, you cart wasnt saved")
    else:
        return render_template("saveCart.html", message="Your cart has been saved")


@app.route('/showCart', methods=['POST', 'GET'])
def showCart():
    return render_template("showCart.html", message=utils.get_cart_info(session['user']))


@app.route('/addToCart', methods=['POST', 'GET'])
def addToCart():
    if (request.method == 'POST'):
        productID = request.form.get('productID')
        store_name = request.form.get('store_name')
        quantity = request.form.get('quantity')
        storeID = request.form.get('storeID')
        try:
            quantity = int(quantity)
        except:
            return render_template("addToCart.html", message="Quantity must be integer")
        if int(quantity) < 1:
            return render_template("addToCart.html", message="Quantity must be positive")
        addToCartOutput = utils.add_product_to_cart(session['user'], product_id=productID, quantity=quantity, store_name=store_name)
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
        addToCartOutput = utils.remove_product_from_cart(session["user"], product_id=productID, quantity=quantity,
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
    # print(f"from checkout: {request.cookies.get('username')}")
    # print(f"from checkout: {session['user']}")
    price = utils.get_cart_info(session['user']).sum
    if (request.method == 'POST'):
        cardNum = request.form.get('cardNum')
        # if(not checkCartAvailability(session['user'])):
        #     return render_template("checkout.html", price=price,message= "Some items are missing")
        # if (not pay(cardNum)):
        #     return render_template("checkout.html", message="Card is not valid")
        # if (not delivery(session['user'])):
        #     return render_template("checkout.html", message="Delivery is not available")
        res = utils.purchase(request.cookies.get('username'), payment_info={"card_number": "123123"}, destination="Ziso 5/3, Beer Sheva")
        if res[0]:
            return render_template("checkout.html", message="Parchase done successfully", price=0)
        else:
            return render_template("checkout.html", message=res[1])
    return render_template("checkout.html", price=0)


@app.route('/openStore', methods=['POST', 'GET'])
def openStore():
    if (request.method == 'POST'):
        storeName = request.form.get('storeName')
        # if(not availableStoreName(storeName)):
        #     return render_template("openStore.html",message= "Store name is not valid")
        if (utils.open_store(storeName, session['user'])):
            return render_template("openStore.html", message="New store has been added")
        else:
            return render_template("openStore.html", message="Something went wrong... try again")
    return render_template("openStore.html")


@app.route('/pastPurchases', methods=['POST', 'GET'])
def pastPurchases():
    return render_template("pastPurchases.html", message=utils.get_user_purchases_history(session['user']))


@app.route('/pastStorePurchases', methods=['POST', 'GET'])
def pastStorePurchases():
    if (request.method == 'POST'):
        storeid = request.form.get('storeid')
        return render_template("pastStorePurchases.html", message=utils.get_store_purchase_history(session["user"], storeid))
    return render_template("pastStorePurchases.html")


@app.route('/addNewProduct', methods=['POST', 'GET'])
def addNewProduct():
    if (request.method == 'POST'):
        storeID = session["store"]
        productID = request.form.get('productID')
        productName = request.form.get('productName')
        productPrice = request.form.get('productPrice')
        productAmout = request.form.get('productAmout')
        productCategory = request.form.get('productCategory')
        productDiscountType = request.form.get('productDiscountType')
        productBuyingType = request.form.get('productBuyingType')
        productDescription = request.form.get('productDescription')
        return render_template("addNewProduct.html", message=
        utils.add_new_product_to_store_inventory(user_name=session["user"], product_id=productID, product_name=productName,
                                           price=productPrice, quantity=productAmout, description=productDescription,
                                           store_name=storeID,
                                           category=productCategory, discount_type=productDiscountType,
                                           buying_type=productBuyingType)[1])
    return render_template("addNewProduct.html")


@app.route('/removeProduct', methods=['POST', 'GET'])
def removeProduct():
    if (request.method == 'POST'):
        storeID = session["store"]
        productID = request.form.get('productID')
        return render_template("removeProduct.html",
                               message=utils.remove_product_from_store_inventory(session["user"], productID, storeID)[1])
    return render_template("removeProduct.html")


@app.route('/editProduct', methods=['POST', 'GET'])
def editProduct():
    if (request.method == 'POST'):
        storeID = session["store"]
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
                               message=utils.edit_product(session["user"], product_id=productID, product_name=productName,
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
        return render_template("purchaseTypes.html", message=utils.get_buying_types(session["user"], storeID)[1])
    return render_template("purchaseTypes.html")


@app.route('/addPurchaseType', methods=['POST', 'GET'])
def addPurchaseType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        return render_template("addPurchaseType.html", message=utils.add_buying_types(session["user"], storeID, details)[1])
    return render_template("addPurchaseType.html")


@app.route('/editPurchaseType', methods=['POST', 'GET'])
def editPurchaseType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        purchaseType = request.form.get('purchaseType')
        details = request.form.get('details')
        return render_template("editPurchaseType.html", message=
        utils.edit_buying_types(session["user"], storeID=storeID, purchaseType=purchaseType, details=details)[1])
    return render_template("editPurchaseType.html")


@app.route('/addDiscountType', methods=['POST', 'GET'])
def addDiscountType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        return render_template("addDiscountType.html", message=utils.add_discount_type(session["user"], storeID, details)[1])
    return render_template("addDiscountType.html")


@app.route('/editDiscountType', methods=['POST', 'GET'])
def editDiscountType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        discountType = request.form.get('discountType')
        details = request.form.get('details')
        return render_template("editDiscountType.html", message=
        utils.edit_discount_type(session["user"], storeID=storeID, discountType=discountType, details=details)[1])
    return render_template("editDiscountType.html")


@app.route('/discountTypes', methods=['POST', 'GET'])
def discountTypes():
    if (request.method == 'POST'):
        return render_template("discountTypes.html", message=request.form.get('storeID')[1])
    return render_template("discountTypes.html")


@app.route('/addPurchasePolicy', methods=['POST', 'GET'])
def addPurchasePolicy():
    if (request.method == 'POST'):
        storeID = session["store"]
        policy_name = request.form.get("buying policy name")
        details = request.form.get('details')
        return render_template("addPurchasePolicy.html",
                               message = utils.add_buying_policy(session["user"], storeID, policy_name, details)[1])
    return render_template("addPurchasePolicy.html")


@app.route('/deletePurchasePolicy', methods=['POST', 'GET'])
def deletePurchasePolicy():
    if (request.method == 'POST'):
        storeID = session["store"]
        policy_name = request.form.get("buying policy name")
        return render_template("deletePurchasePolicy.html",
                               message=utils.delete_buying_policy(session["user"], storeID, policy_name)[1])
    return render_template("deletePurchasePolicy.html")


@app.route('/deleteDiscountPolicy', methods=['POST', 'GET'])
def deleteDiscountPolicy():
    if (request.method == 'POST'):
        storeID = session["store"]
        policy_name = request.form.get("discount policy name")
        return render_template("deleteDiscountPolicy.html",
                               message=utils.delete_discount_policy(session["user"], storeID, policy_name)[1])
    return render_template("deleteDiscountPolicy.html")


@app.route('/showPurchasePolicy', methods=['POST', 'GET'])
def showPurchasePolicy():
    if (request.method == 'POST'):
        storeID = session["store"]
        return render_template("showPurchasePolicy.html",
                               message=utils.show_buying_policy(session["user"], storeID)[1])
    return render_template("showPurchasePolicy.html")


@app.route('/showDiscountPolicy', methods=['POST', 'GET'])
def showDiscountPolicy():
    if (request.method == 'POST'):
        storeID = session["store"]
        return render_template("showDiscountPolicy.html",
                               message=utils.show_discount_policy(session["user"], storeID)[1])
    return render_template("showDiscountPolicy.html")


@app.route('/editPurchasePolicy', methods=['POST', 'GET'])
def editPurchasePolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        purchasePolicy = request.form.get('purchaseType')
        details = request.form.get('details')
        return render_template("editPurchasePolicy.html", message=
        utils.edit_buying_policy(session["user"], storeID=storeID, purchasePolicy=purchasePolicy, details=details)[1])
    return render_template("editPurchasePolicy.html")


@app.route('/purchasePolicy', methods=['POST', 'GET'])
def purchasePolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("purchasePolicy.html", message=utils.get_buying_policy(session["user"], storeID)[1])
    return render_template("purchasePolicy.html")


@app.route('/addTermDiscount', methods=['POST', 'GET'])
def addTermDiscount():
    if (request.method == 'POST'):
        storeID = session["store"]
        discount_name = request.form.get('discount_name')
        discount_term = request.form.get('discount_term')
        discount_value = request.form.get('discount_value')
        return render_template("addTermDiscount.html",
                               message=utils.add_term_discount(session["user"], storeID,
                                                         discount_name, discount_value, discount_term)[1])
    return render_template("addTermDiscount.html")


@app.route('/addSimpleDiscount', methods=['POST', 'GET'])
def addSimpleDiscount():
    if (request.method == 'POST'):
        storeID = session["store"]
        discount_name = request.form.get('discount_name')
        discount_value = request.form.get('discount_value')
        return render_template("addSimpleDiscount.html",
                               message=utils.add_simple_discount(session["user"], storeID,
                                                           discount_name, discount_value)[1])
    return render_template("addSimpleDiscount.html")


@app.route('/editDiscountPolicy', methods=['POST', 'GET'])
def editDiscountPolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        discountPolicy = request.form.get('discountPolicy')
        details = request.form.get('details')
        return render_template("editDiscountPolicy.html", message=
        utils.edit_discount_policy(session["user"], storeID=storeID, discountPolicy=discountPolicy, details=details)[1])
    return render_template("editDiscountPolicy.html")


@app.route('/discountPolicy', methods=['POST', 'GET'])
def discountPolicy():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("discountPolicy.html", message=utils.get_discount_policy(session["user"], storeID)[1])
    return render_template("discountPolicy.html")


@app.route('/getEmployeeDetails', methods=['POST', 'GET'])
def getEmployeeDetails():
    if (request.method == 'POST'):
        storeid = session["store"]
        employeeid = request.form.get('employeeid')
        return render_template("getEmployeeDetails.html",
                               message=utils.get_employee_details(session["user"], storeid, employeeid)[1])
    return render_template("getEmployeeDetails.html")


@app.route('/getEmployeePermissions', methods=['POST', 'GET'])
def getEmployeePermissions():
    if (request.method == 'POST'):
        storeid = session["store"]
        employeeid = request.form.get('employeeid')
        return render_template("getEmployeePermissions.html",
                               message=utils.get_employee_permissions(session["user"], storeid, employeeid)[1])
    return render_template("getEmployeePermissions.html")


def initialize_system():
    store_name = "store"
    admin = "admin"
    niv = "niv"
    a = "a"
    utils.register(admin, admin, 20)
    utils.register(niv, niv, 20)
    utils.register(a, a, 20)
    username_hash = utils.log_in(admin, admin)[1]
    niv_hash = utils.log_in(niv, niv)[1]

    utils.open_store(store_name, username_hash)
    utils.assign_store_owner(username_hash, a, store_name)
    utils.add_new_product_to_store_inventory(username_hash, "1", "1", 1, 50, "no description", store_name, "dairy",
                                             None, None)
    utils.add_product_to_cart(user_name=niv_hash, store_name=store_name, product_id="1", quantity=1)
    utils.assign_store_manager(username_hash, niv, store_name)

    # utils.purchase(user_name=niv_hash, payment_info={"card_number": "123123"}, destination="Ziso 5/3, Beer Sheva")

    utils.log_out(username_hash)
    utils.log_out(niv_hash)


if __name__ == '__main__':
    initialize_system()
    socketio.run(app=app, debug=True)
