import argparse
from unittest import TestCase

import OnlineStore.src.presentation_layer.utils as utils

users_num = 10000
prod_num = 1000
users = dict()

payment_info = {"card_number": "123123", "year": "2024", "month": "3", "ccv": "111", "id": "205557564",
                "holder": "Niv"}
buyer_information = {"city": "Israel", "country": "Beer Sheva", "zip": "8538600",
                     "address": "ziso 5/3 beer sheva, israel",
                     "name": 'Niv'}

parser = argparse.ArgumentParser(description='Workshop 212')
parser.add_argument('--init_file', action='store', default="init.json", help="Initialization file")
parser.add_argument('--config_file', action='store', default="config.json", help="Config file")
parser.add_argument('--clean', action='store_true', default="false", help="clean database")
args = parser.parse_args()

if utils.initialize_system(init_file=args.init_file, config_file=args.config_file, clean_db=False):
    for i in range(0, users_num):
        x = utils.register(f'u{i}', f'u{i}', i)
        if x[0]:
            print(f'reg: {i}')

    for i in range(0, users_num):
        user_hash = utils.log_in(f'u{i}', f'u{i}')
        if user_hash[0]:
            users[f'u{i}'] = user_hash[1]
        else:
            print('fail login')
            continue

        if i % 10 == 0:
            x = utils.open_store(f's{i}', users[f'u{i}'])
            if x[0]:
                print(f'store: {i}')
            for j in range(prod_num):
                x = utils.add_new_product_to_store_inventory(users[f'u{i}'], f'p{j}', f'p{j}', 1, 10, f'descrp: p{j}',
                                                             f's{i}', 'test cat')
                # if x[0] and j % 100 == 0:
                #     print(f'store: {i}, store: {j}')
            print(f'store: {i} done')

else:
    raise Exception("couldn't initialize")


# class TestLoad(TestCase):
#     def test_purchase(self):
#         #     for i in range(users_num):
#         #         if i % 10 == 0:
#         #             print(f'purchase: {i}')
#         #             buyer = users[f'u{i + 1}']
#         #             # buyer = utils.log_in(f'u{i + 1}', f'u{i + 1}')
#         #             for j in range(prod_num):
#         #                 utils.add_product_to_cart(buyer, f'p{j}', 1, f's{i}')
#         #                 utils.purchase(buyer, payment_info, buyer_information)
#         #             pur = utils.get_user_purchases_history(buyer)[1]
#         #             self.assertTrue(len(pur) == prod_num)
#         print("done!!!")

# def test_items(self):
