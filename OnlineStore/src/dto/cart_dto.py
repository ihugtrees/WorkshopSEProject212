from OnlineStore.src.domain_layer.user.cart import Cart
from OnlineStore.src.dto.basket_dto import BasketDTO
import OnlineStore.src.data_layer.user_entity as db_ent


class CartDTO:
    def __init__(self, cart: Cart):
        self.basket_dict = dict()
        for store_name_key in cart.basket_dict.keys():
            self.basket_dict[store_name_key] = BasketDTO(cart.basket_dict[store_name_key])
        self.sum = 0

    def from_dto_to_db(self):
        db_cart: db_ent.Cart = db_ent.Cart(basket_dict=[])
        for store_name_key in self.basket_dict.keys():
            products_dict = list()
            for product_name in self.basket_dict[store_name_key].products_dict.keys():
                temp = self.basket_dict[store_name_key].products_dict
                products_dict.append(db_ent.BasketItem(product_name=product_name, quantity=temp[product_name]))
            db_cart.basket_dict.append(db_ent.Basket(store_name=store_name_key, products_dict=products_dict))