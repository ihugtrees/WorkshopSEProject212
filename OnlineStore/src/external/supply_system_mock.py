import datetime

from OnlineStore.src.dto.cart_dto import CartDTO
import http
import requests


# the supply system rejects all the deliveries to haifa

def supply(cart: CartDTO, user_information) -> str:
    # h1: http.client.HTTPConnection = http.client.HTTPConnection('https://cs-bgu-wsep.herokuapp.com', 443)
    # h1.request(method='GET', url="/", body={'action_type': 'handshake'})
    # resp = h1.getresponse()
    url = 'https://cs-bgu-wsep.herokuapp.com/'
    response = requests.post(url=url, data={"action_type": "handshake"})
    if str(response.content) != "OK":
        raise Exception("Handshake went wrong")
    response = requests.post(url, data={"action_type": "supply", "name": "niv", "address": "12323", "city": "Beer Sheva", "country": "Israel", "zip": "8538600"})
    transaction_id = response.content
    if transaction_id == -1:
        raise Exception("Delivery system rejected the delivery")
    print(f"Transaction id:{int(response.content)}")
    return transaction_id

    # if user_information == "haifa":
    #     raise Exception("Delivery system rejected the delivery")
    # else:
    #     return (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y, %H:%M")


# print(address_supply_system(None, 'lol'))
