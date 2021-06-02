import eventlet
from flask import (Flask, render_template, request, redirect, session)
from flask_socketio import SocketIO, join_room
import argparse
import json

import OnlineStore.src.presentation_layer.utils as utils
from OnlineStore.src.communication_layer import publisher
from OnlineStore.src.dto.cart_dto import CartDTO
from OnlineStore.src.presentation_layer import convert_data

# from gevent import monkey
app = Flask(__name__)
app.secret_key = 'ItShouldBeAnythingButSecret'  # you can set any secret key but remember it should be secret

socketio = SocketIO(app)


@socketio.on('join')
def on_join(data):
    join_room(session.get('username'))


@socketio.on('send messages')
def on_send_messages(data):
    publisher.send_messages(session.get('username'))


@socketio.on("connect")
def on_connect():
    print(f"Client {session.get('username')} connected")


@socketio.on('disconnect')
def socket_disconnect():
    # if utils.is_user_guest(session["username"]):
    #     utils.exit_the_site(session["username"])
    print(f"Client {session.get('username')} disconnected")


def convert_purchase_to_string(purchase):
    pass


def convert_cartDTO_to_list_of_string(cartDTO: CartDTO):
    ans = list()
    for b in cartDTO.basket_dict:
        ans.append(b + ": ")
        p_dict = cartDTO.basket_dict[b].products_dict
        for p in p_dict:
            ans.append("product name: " + p + " quantity: " + str(p_dict[p]))
    return ans


def display_answer(ans):
    if ans is None:
        return "done"
    else:
        return ans


# creating route for login
@app.route('/', methods=['POST', 'GET'])
def web_login():
    if request.method == 'POST':
        # if 'user' in session and session['user'] is not None:
        #     return redirect('/wronglogin')  # maybe bug
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
        elif username_hash[1] == "User Already Logged In":
            session['username'] = username
            session['user'] = username_hash[1]
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
    if request.method == 'POST' and 'user' in session and session['user'] is not None:
        user = session['user']
        store_id = request.form.get('storeID')
        resp = utils.userIsStoreOwner(user, store_id)
        if resp[0]:
            session["store"] = store_id
            return render_template("manageStoreOwner.html")
        if utils.userIsStoreManager(user, store_id)[0]:
            session["store"] = store_id
            return render_template("dashboardStoreManager.html")
        return render_template("dashboard.html", welcome=f"Hi {session['username']} What would You like to do?")
    if 'user' in session and session['user'] is not None:
        session["store"] = "None" if "store" not in session else session["store"]
        return render_template("dashboard.html", message=session["store"],
                               welcome=f"Hi {session['username']} What would You like to do?")
    return '<h1>You are not logged in.</h1>'  # if the user is not in the session


@app.route('/guest_dashboard', methods=['POST', 'GET'])
def guest_dashboard():
    ans = utils.get_into_site()
    if ans[0]:
        session['user'] = ans[1]
        session['username'] = ans[1]
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
    session['username'] = None
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
            ans = utils.register(username, password, age)
            return render_template("signup.html", message=display_answer(ans[1]))

    return render_template("signup.html")


@app.route('/changePassword', methods=['POST', 'GET'])
def changePassword():
    if (request.method == 'POST'):
        old_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        return render_template("changePassword.html", message=display_answer(
            utils.change_password(session["user"], old_password, new_password)[1]))
    return render_template("changePassword.html")


@app.route('/addstoremanager', methods=['POST', 'GET'])
def addstoremanager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session["store"]
        return render_template("addstoremanager.html",
                               message=display_answer(utils.assign_store_manager(session["user"], userid, storeid)[1]))
    return render_template("addstoremanager.html")


@app.route('/removeStoreManager', methods=['POST', 'GET'])
def removeStoreManager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session["store"]
        return render_template("removeStoreManager.html",
                               message=display_answer(utils.remove_store_manager(session["user"], userid, storeid)[1]))
    return render_template("removeStoreManager.html")


@app.route('/removeStoreOwner', methods=['POST', 'GET'])
def removeStoreOwner():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session['store']
        return render_template("removeStoreOwner.html",
                               message=display_answer(utils.remove_store_owner(session["user"], userid, storeid)[1]))
    return render_template("removeStoreOwner.html")


@app.route('/editStoreManager', methods=['POST', 'GET'])
def editStoreManager():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session["store"]
        permissionUpdate = request.form.get('permissionUpdate')
        return render_template("editStoreManager.html", message=
        display_answer(utils.edit_store_manager_permissions(session["user"], userid, permissionUpdate, storeid)[1]))
    return render_template("editStoreManager.html")


@app.route('/addStoreOwner', methods=['POST', 'GET'])
def addStoreOwner():
    if (request.method == 'POST'):
        userid = request.form.get('userid')
        storeid = session["store"]
        return render_template("addStoreOwner.html",
                               message=display_answer(utils.assign_store_owner(session["user"], userid, storeid)[1]))
    return render_template("addStoreOwner.html")


@app.route('/productInfo', methods=['POST', 'GET'])
def productInfo():
    if request.method == 'POST':
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
        if storeInfo[0]:
            return render_template("storeInfo.html", storeID=storeID, storeInfo=storeInfo[1])
        return render_template("storeInfo.html", storeID=storeID, warning="Something went wrong...")
    return render_template("storeInfo.html")


@app.route('/prodByName', methods=['POST', 'GET'])
def prodByName():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        minprice = request.form.get('minprice')
        maxprice = request.form.get('maxprice')
        prating = request.form.get('prating')
        srating = request.form.get('srating')
        try:
            filters = utils.create_filters(minprice, maxprice, prating, category, srating)
        except Exception as e:
            return render_template("prodByName.html", warning="prices and ratings must be numbers" + e.args[0])
        products = utils.search_product_by_name(name, filters)
        if products[0]:
            return render_template("prodByName.html", products=products[1])
        else:
            return render_template("prodByName.html", warning=products[1])
    return render_template("prodByName.html")


@app.route('/prodByCategory', methods=['POST', 'GET'])
def prodByCategory():
    if request.method == 'POST':
        category = request.form.get('category')
        minprice = request.form.get('minprice')
        maxprice = request.form.get('maxprice')
        prating = request.form.get('prating')
        srating = request.form.get('srating')
        products = utils.search_product_by_category(category,
                                                    utils.create_filters(minprice, maxprice, prating, category,
                                                                         srating))
        if products[0]:
            return render_template("prodByCategory.html", products=products[1])
        else:
            return render_template("prodByCategory.html", warning=products[1])
    return render_template("prodByCategory.html")


@app.route('/prodByKeyword', methods=['POST', 'GET'])
def prodByKeyword():
    if request.method == 'POST':
        key = request.form.get('key')
        category = request.form.get('category')
        minprice = request.form.get('minprice')
        maxprice = request.form.get('maxprice')
        prating = request.form.get('prating')
        srating = request.form.get('srating')
        products = utils.search_product_by_keyword(key,
                                                   utils.create_filters(minprice, maxprice, prating, category, srating))
        if products[0]:
            return render_template("prodByKeyword.html", products=products[1])
        else:
            return render_template("prodByKeyword.html", warning=products[1])
    return render_template("prodByKeyword.html")


@app.route('/saveCart', methods=['POST', 'GET'])
def saveCart():
    if 'user' not in session or not utils.save_cart(session['user']):
        return render_template("saveCart.html", message="Error occured, you cart wasnt saved")
    else:
        return render_template("saveCart.html", message="Your cart has been saved")


@app.route('/showCart', methods=['POST', 'GET'])
def showCart():
    return render_template("showCart.html",
                           cart_list=convert_cartDTO_to_list_of_string(utils.get_cart_info(session['user'])))


@app.route('/messageBox', methods=['POST', 'GET'])
def messageBox():
    ans = utils.get_user_history_message(session["user"])
    return render_template("messageBox.html", message_list=convert_data.convert_messages(ans[1]))


@app.route('/addToCart', methods=['POST', 'GET'])
def addToCart():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        productID = request.form.get('productID')
        quantity = request.form.get('quantity')
        try:
            quantity = int(quantity)
        except:
            return render_template("addToCart.html", message="Quantity must be integer")
        if int(quantity) < 1:
            return render_template("addToCart.html", message="Quantity must be positive")
        addToCartOutput = utils.add_product_to_cart(session['user'], product_id=productID, quantity=quantity,
                                                    store_name=storeID)
        if addToCartOutput[0]:
            return render_template("addToCart.html", message="Item has been added to cart")
        else:
            return render_template("addToCart.html", message=display_answer(addToCartOutput[1]))
    return render_template("addToCart.html")


@app.route('/removeFromCart', methods=['POST', 'GET'])
def removeFromCart():
    if (request.method == 'POST'):
        storeID = request.form.get("storeID")
        productID = request.form.get('productID')
        quantity = request.form.get('quantity')
        try:
            quantity = int(quantity)
        except:
            return render_template("removeFromCart.html", message="Quantity must be integer")
        if (int(quantity) < 1):
            return render_template("removeFromCart.html", message="Quantity must be positive")
        removeToCartOutput = utils.remove_product_from_cart(session["user"], productID, quantity,
                                                            storeID)
        if (removeToCartOutput[0]):
            return render_template("removeFromCart.html", message="Item has been removed from cart")
        else:
            return render_template("removeFromCart.html", message="Error")
    return render_template("removeFromCart.html")


@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    # print(f"from checkout: {request.cookies.get('username')}")
    # print(f"from checkout: {session['user']}")
    price = utils.get_cart_info(session['user']).sum
    if request.method == 'POST':
        card_num = request.form.get('card_num')
        year = request.form.get("year") if request.form.get("year") != '' else None
        month = request.form.get("month") if request.form.get("month") != '' else None
        ccv = request.form.get("ccv") if request.form.get("ccv") != '' else None
        card_holder_id = request.form.get("card_holder_id") if request.form.get("card_holder_id") != '' else None
        city = request.form.get("city") if request.form.get("city") != '' else None
        country = request.form.get("country") if request.form.get("country") != '' else None
        zip_code = request.form.get("zip") if request.form.get("zip") != '' else None
        holder_name = request.form.get("holder_name") if request.form.get("holder_name") != '' else None
        address = request.form.get("address") if request.form.get("address") != '' else None

        payment_info = {"card_number": card_num, "year": year, "month": month, "ccv": ccv, "id": card_holder_id,
                        "holder": holder_name}
        buyer_information = {"city": city, "country": country, "zip": zip_code, "address": address,
                             "name": session["username"]}
        # if(not checkCartAvailability(session['user'])):
        #     return render_template("checkout.html", price=price,message= "Some items are missing")
        # if (not pay(cardNum)):
        #     return render_template("checkout.html", message="Card is not valid")
        # if (not delivery(session['user'])):
        #     return render_template("checkout.html", message="Delivery is not available")
        ans = utils.purchase(session["user"], payment_info=payment_info, buyer_information=buyer_information)
        if ans[0]:
            return render_template("checkout.html", message="Parchase done successfully", price=0)
        else:
            return render_template("checkout.html", message=ans[1])
    return render_template("checkout.html", price=price)

@app.route('/makeOffer', methods=['POST', 'GET'])
def makeOffer():
    price = utils.get_cart_info(session['user']).sum
    if request.method == 'POST':
        card_num = request.form.get('card_num')
        year = request.form.get("year")
        month = request.form.get("month")
        ccv = request.form.get("ccv")
        card_holder_id = request.form.get("card_holder_id")
        city = request.form.get("city")
        country = request.form.get("country")
        zip_code = request.form.get("zip")
        holder_name = request.form.get("holder_name")
        address = request.form.get("address")
        store = request.form.get("store_name")
        product = request.form.get("product_name")
        quantity = request.form.get("quantity")
        price = request.form.get("price")

        payment_info = {"card_number": card_num, "year": year, "month": month, "ccv": ccv, "id": card_holder_id,
                        "holder": holder_name}
        buyer_information = {"city": city, "country": country, "zip": zip_code, "address": address,
                             "name": session["username"]}

        return render_template("makeOffer.html", message=
        display_answer(utils.make_offer(session["user"], store, product, int(quantity), int(price), payment_info, buyer_information)[1]))
    return render_template("makeOffer.html", price=price)


@app.route('/openStore', methods=['POST', 'GET'])
def openStore():
    if (request.method == 'POST'):
        storeName = request.form.get('storeName')
        # if(not availableStoreName(storeName)):
        #     return render_template("openStore.html",message= "Store name is not valid")
        resp = utils.open_store(storeName, session['user'])
        if resp[0]:
            return render_template("openStore.html", message="New store has been added")
        else:
            return render_template("openStore.html", message=resp[1])
    return render_template("openStore.html")


@app.route('/pastPurchases', methods=['POST', 'GET'])
def pastPurchases():
    purchase_list = utils.get_user_purchases_history(session['user'])
    if purchase_list[0]:
        return render_template("pastPurchases.html", message="Your purchase history", purchase_list=purchase_list[1])
    else:
        return render_template("pastPurchases.html", message="Error: " + purchase_list[1])


@app.route('/pastStorePurchases', methods=['POST', 'GET'])
def pastStorePurchases():
    if 'store' in session and session["store"] is not None:
        purchase_list = utils.get_store_purchase_history(session["user"], session["store"])
        if purchase_list[0]:
            return render_template("pastStorePurchases.html",
                                   message="Purchase history", purchase_list=purchase_list[1])
        else:
            return render_template("pastStorePurchases.html", message="Error: " + purchase_list[1])

    return render_template("pastStorePurchases.html")


# @app.route('/addNewProduct', methods=['POST', 'GET'])
# def addNewProduct():
#     if (request.method == 'POST'):
#         storeID = request.form.get('storeID')
#         productID = request.form.get('productID')
#         productName = request.form.get('productName')
#         productPrice = request.form.get('productPrice')
#         productAmout = request.form.get('productAmout')
#         productCategory = request.form.get('productCategory')
#         productDiscountType = request.form.get('productDiscountType')
#         productBuyingType = request.form.get('productBuyingType')
#         productDescription = request.form.get('productDescription')
#         return render_template("addNewProduct.html", message=
#         add_new_product_to_store_inventory(user_name=session["user"], product_id=productID, product_name=productName,
#                                            price=productPrice, quantity=productAmout, description=productDescription,
#                                            store_name=storeID,
#                                            category=productCategory, discount_type=productDiscountType,
#                                            buying_type=productBuyingType)[1])
#     return render_template("addNewProduct.html")


@app.route('/removeProduct', methods=['POST', 'GET'])
def removeProduct():
    if (request.method == 'POST'):
        storeID = session["store"]
        productID = request.form.get('productID')
        return render_template("removeProduct.html",
                               message=display_answer(
                                   utils.remove_product_from_store_inventory(session["user"], productID, storeID)[1]))
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
                               message=display_answer(
                                   utils.edit_product(session["user"], product_id=productID, product_name=productName,
                                                      price=productPrice, quantity=productAmout,
                                                      description=productDescription,
                                                      store_name=storeID, category=productCategory,
                                                      discount_type=productDiscountType, buying_type=productBuyingType)[
                                       1]))
    return render_template("editProduct.html")


@app.route('/purchaseTypes', methods=['POST', 'GET'])
def purchaseTypes():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        return render_template("purchaseTypes.html",
                               message=display_answer(utils.get_buying_types(session["user"], storeID)[1]))
    return render_template("purchaseTypes.html")


@app.route('/addPurchaseType', methods=['POST', 'GET'])
def addPurchaseType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        return render_template("addPurchaseType.html",
                               message=display_answer(utils.add_buying_types(session["user"], storeID, details)[1]))
    return render_template("addPurchaseType.html")


@app.route('/editPurchaseType', methods=['POST', 'GET'])
def editPurchaseType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        purchaseType = request.form.get('purchaseType')
        details = request.form.get('details')
        return render_template("editPurchaseType.html", message=
        display_answer(
            utils.edit_buying_types(session["user"], storeID=storeID, purchaseType=purchaseType, details=details)[1]))
    return render_template("editPurchaseType.html")


@app.route('/addDiscountType', methods=['POST', 'GET'])
def addDiscountType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        details = request.form.get('details')
        return render_template("addDiscountType.html",
                               message=display_answer(utils.add_discount_type(session["user"], storeID, details)[1]))
    return render_template("addDiscountType.html")


@app.route('/editDiscountType', methods=['POST', 'GET'])
def editDiscountType():
    if (request.method == 'POST'):
        storeID = request.form.get('storeID')
        discountType = request.form.get('discountType')
        details = request.form.get('details')
        return render_template("editDiscountType.html", message=
        display_answer(
            utils.edit_discount_type(session["user"], storeID=storeID, discountType=discountType, details=details)[1]))
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
                               message=display_answer(
                                   utils.add_buying_policy(session["user"], storeID, policy_name, details)[1]))
    return render_template("addPurchasePolicy.html")


@app.route('/createBuyingOffer', methods=['POST', 'GET'])
def createBuyingOffer():
    if (request.method == 'POST'):
        storeID = session["store"]
        product_name = request.form.get("product_name")
        minimum = request.form.get("minimum_price")
        return render_template("createBuyingOffer.html",
                               message=display_answer(
                                   utils.open_product_to_offer(session["user"], storeID, product_name, minimum)[1]))
    return render_template("createBuyingOffer.html")


@app.route('/addNewProduct', methods=['POST', 'GET'])
def addNewProduct():
    if (request.method == 'POST'):
        storeID = session['store']
        productID = request.form.get("productID")
        product_Name = request.form.get('productName')
        product_Price = request.form.get("productPrice")
        product_Amount = request.form.get("productAmount")
        product_Description = request.form.get("productDescription")
        product_Category = request.form.get("productCategory")
        return render_template("addNewProduct.html",
                               message=display_answer(
                                   utils.add_new_product_to_store_inventory(session["user"], productID,
                                                                            product_Name, product_Price, product_Amount,
                                                                            product_Description, storeID,
                                                                            product_Category)[1]))
    return render_template("addNewProduct.html")


@app.route('/deletePurchasePolicy', methods=['POST', 'GET'])
def deletePurchasePolicy():
    if (request.method == 'POST'):
        storeID = session["store"]
        policy_name = request.form.get("buying policy name")
        return render_template("deletePurchasePolicy.html",
                               message=display_answer(
                                   utils.delete_buying_policy(session["user"], storeID, policy_name)[1]))
    return render_template("deletePurchasePolicy.html")


@app.route('/deleteDiscountPolicy', methods=['POST', 'GET'])
def deleteDiscountPolicy():
    if (request.method == 'POST'):
        storeID = session["store"]
        policy_name = request.form.get("discount policy name")
        return render_template("deleteDiscountPolicy.html",
                               message=display_answer(
                                   utils.delete_discount_policy(session["user"], storeID, policy_name)[1]))
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
                               message=display_answer(utils.add_term_discount(session["user"], storeID,
                                                                              discount_name, discount_value,
                                                                              discount_term)[1]))
    return render_template("addTermDiscount.html")


@app.route('/combineDiscount', methods=['POST', 'GET'])
def CombineDiscount():
    if (request.method == 'POST'):
        storeID = session["store"]
        discount_name1 = request.form.get('discount_name1')
        discount_name2 = request.form.get('discount_name2')
        new_name = request.form.get("new_name")
        operator = request.form.get("operator")
        return render_template("combineDiscount.html",
                               message=display_answer(
                                   utils.combine_discount(session["user"], storeID, discount_name1, discount_name2,
                                                          operator, new_name)[1]))
    return render_template("combineDiscount.html")


@app.route('/addSimpleDiscount', methods=['POST', 'GET'])
def addSimpleDiscount():
    if (request.method == 'POST'):
        storeID = session["store"]
        discount_name = request.form.get('discount_name')
        discount_value = request.form.get('discount_value')
        ans = utils.add_simple_discount(session["user"], storeID,
                                        discount_name, discount_value)
        if ans[0]:
            return render_template("addSimpleDiscount.html",
                                   message="discount added successfully")
        else:
            return render_template("addSimpleDiscount.html",
                                   message=ans[1])
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
                               message=display_answer(
                                   utils.get_employee_details(session["user"], storeid, employeeid)[1]))
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
    import os
    if os.path.exists("database.sqlite"):
        os.remove("database.sqlite")
    else:
        print("The file does not exist")

    from OnlineStore.src.data_layer.user_entity import db
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
    store_name = "store"
    admin = "admin"
    niv = "niv"
    a = "a"
    manager1 = "manager1"
    b = "b"
    payment_info = {"card_number": "123123", "year": "2024", "month": "3", "ccv": "111", "id": "205557564",
                    "holder": "Niv"}
    buyer_information = {"city": "Israel", "country": "Beer Sheva", "zip": "8538600",
                         "address": "ziso 5/3 beer sheva, israel",
                         "name": niv}
    utils.register(admin, admin, 20)
    utils.register(niv, niv, 20)
    utils.register(a, a, 20)
    utils.register(manager1, manager1, 20)
    utils.register(b, b, 20)
    admin_hash = utils.log_in(admin, admin)[1]
    niv_hash = utils.log_in(niv, niv)[1]
    a_hash = utils.log_in(a, a)[1]
    manager_hash = utils.log_in(manager1, manager1)[1]

    utils.open_store("store1", manager_hash)
    utils.open_store(store_name, admin_hash)
    utils.assign_store_owner(admin_hash, a, store_name)
    utils.assign_store_owner(a_hash, b, store_name)
    utils.add_new_product_to_store_inventory(manager_hash, "1", "1", 1, 50, "no description", "store1", "dairy")
    utils.add_new_product_to_store_inventory(admin_hash, "1", "1", 1, 50, "no description", store_name, "dairy")
    utils.add_new_product_to_store_inventory(admin_hash, "milk", "milk", 50, 50, "milk description", store_name,
                                             "milky")
    utils.add_simple_discount(admin_hash, store_name, "a", "milk 20")
    utils.add_simple_discount(admin_hash, store_name, "b", "milk 30")
    utils.add_product_to_cart(user_name=admin_hash, store_name=store_name, product_id="milk", quantity=4)
    utils.add_product_to_cart(user_name=admin_hash, store_name=store_name, product_id="milk", quantity=4)

    utils.remove_product_from_cart(user_name=admin_hash, store_name=store_name, product_id="milk", quantity=4)
    utils.remove_product_from_cart(user_name=admin_hash, store_name=store_name, product_id="milk", quantity=4)
    utils.add_product_to_cart(user_name=niv_hash, store_name=store_name, product_id="1", quantity=1)

    # utils.purchase(user_name=niv_hash, payment_info=payment_info, buyer_information=buyer_information)


    utils.add_product_to_cart(user_name=niv_hash, store_name=store_name, product_id="1", quantity=1)
    # utils.add_simple_discount(admin_hash, store_name, "a", "milk 20")
    # utils.add_simple_discount(admin_hash, store_name, "b", "milk 30")
    # utils.add_product_to_cart(user_name=admin_hash, store_name=store_name, product_id="milk", quantity=4)
    # utils.add_product_to_cart(user_name=niv_hash, store_name=store_name, product_id="1", quantity=1)
    #
    # utils.purchase(user_name=niv_hash, payment_info=payment_info, buyer_information=buyer_information)
    # utils.add_product_to_cart(user_name=niv_hash, store_name=store_name, product_id="1", quantity=1)
    # utils.purchase(user_name=niv_hash, payment_info=payment_info, buyer_information=buyer_information)
    # utils.add_product_to_cart(user_name=niv_hash, store_name=store_name, product_id="1", quantity=1)
    # utils.add_product_to_cart(user_name=niv_hash, store_name="store1", product_id="1", quantity=1)

    utils.log_out(manager_hash)
    utils.log_out(admin_hash)

    utils.purchase(user_name=niv_hash, payment_info=payment_info, buyer_information=buyer_information)
    utils.add_product_to_cart(user_name=niv_hash, store_name=store_name, product_id="1", quantity=1)
    utils.add_product_to_cart(user_name=niv_hash, store_name="store1", product_id="1", quantity=1)
    utils.log_out(niv_hash)
    utils.log_out(a_hash)


if __name__ == '__main__':
    # eventlet.monkey_patch()
    # monkey.patch_all()
    # initialize_system()
    # socketio.run(app=app, debug=True, certfile='cert.pem', keyfile='key.pem', port=8443, use_reloader=False)
    # initialize_system()
    parser = argparse.ArgumentParser(description='Workshop 212')
    parser.add_argument('--init_file',action='store',default="init.json",help="Initialization file")
    args = parser.parse_args()
    utils.initialize_system(file=args.init_file)
    socketio.run(app=app, debug=True, certfile='cert.pem', keyfile='key.pem', port=8443, use_reloader=False)
    # socketio.run(app=app, debug=True)
