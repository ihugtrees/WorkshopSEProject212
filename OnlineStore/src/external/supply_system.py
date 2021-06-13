from OnlineStore.src.dto.cart_dto import CartDTO
from OnlineStore.src.external.urlVar import supply_url
import http
import requests


class SupplySystem:

    def supply(self, buyer_information: dict) -> str:
        url = "https://cs-bgu-wsep.herokuapp.com/"
        response = requests.post(url=url, data={"action_type": "handshake"})
        # print(str(response.content))
        if str(response.content) != "b'OK'":
            raise Exception("Handshake went wrong")
        response = requests.post(url, data={"action_type": "supply", "name": buyer_information["name"],
                                            "address": buyer_information["address"], "city": buyer_information["city"],
                                            "country": buyer_information["country"], "zip": buyer_information["zip"]})
        transaction_id = int(response.content)
        if transaction_id == -1:
            raise Exception("Delivery system rejected the delivery")
        print(f"Transaction id:{int(response.content)}")
        return transaction_id


    def cancel_supply(self, transaction_id: int) -> None:
        url = "https://cs-bgu-wsep.herokuapp.com/"
        response = requests.post(url=url, data={"action_type": "cancel_supply", "transaction_id": transaction_id})
        if str(response.content) != "b'OK'":
            raise Exception("Handshake went wrong")
        response = requests.post(url, data={"action_type": "cancel_supply", "transaction_id": transaction_id})
        suc_flag = int(response.content)
        if suc_flag == -1:
            raise Exception("Something went wrong with canceling the supply")