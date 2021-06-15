from threading import Lock

from pony.orm import db_session

from OnlineStore.src.data_layer import user_entity


class Product:
    def __init__(self, product_id, product_name, quantity, price, category="null", discount_type=None,
                 buying_type=None):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = int(quantity)
        self.description = ""
        self.discount_type = discount_type
        self.buying_type = buying_type
        self.price = int(price)
        self.category = category
        self.rating = 0
        self.lock = Lock()

    # TODO work with db

    def take_quantity(self, num_to_take, store_name):
        if num_to_take <= 0:
            raise Exception("Negative or zero quantity\n")
        self.quantity = user_entity.Product.get(store=store_name, product_id=self.product_name).quantity
        if self.quantity < num_to_take:
            raise Exception("There are only " + str(self.quantity) + " from " + self.product_name + " in the store.\n")
        self.quantity -= num_to_take
        user_entity.Product.get(store=store_name, product_id=self.product_name).quantity -= num_to_take


    # TODO work with db
    def return_quantity(self, num_to_take, store_name):
        if num_to_take <= 0:
            raise Exception("impossible to return negative amount")
        self.lock.acquire()
        user_entity.Product.get(store=store_name, product_id=self.product_name).quantity += num_to_take
        self.quantity += num_to_take
        self.lock.release()

    def calculate_product_sum(self, quantity: int) -> int:
        # TODO FOR NOW ONLY QUANTITY*PRICE
        return self.price * quantity

    @db_session
    def add_quantity(self, quant, store_name):
        if quant <= 0:
            raise Exception("cant add less than one quantity")
        self.quantity += quant
        user_entity.Product.get(store=store_name, product_id=self.product_name).quantity += quant

    @db_session
    def edit_product_description(self, product_description, store_name):
        if type(product_description) != str:
            raise Exception("description must be string")
        self.description = product_description
        user_entity.Product.get(store=store_name, product_id=self.product_name).description = product_description
        #product_db.description = product_description



    def change_quantity(self, store_name, product_name, quantity, ):
        pass
