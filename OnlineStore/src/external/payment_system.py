import requests


# the supply system rejects all the deliveries to haifa

def pay(payment_info: dict) -> str:
    url = 'https://cs-bgu-wsep.herokuapp.com/'
    response = requests.post(url=url, data={"action_type": "handshake"})
    if str(response.content) != "b'OK'":
        raise Exception("Handshake went wrong")
    response = requests.post(url=url, data={"action_type": "pay", "card_number":payment_info["card_number"],
                                            "month": payment_info["month"], "year": payment_info["year"],
                                            "holder": payment_info["holder"], "ccv": payment_info["ccv"],
                                            "id": payment_info["id"]})
    transaction_id = int(response.content)
    if transaction_id == -1:
        raise Exception("Payment system rejected the payment")
    print(f"Transaction id:{int(response.content)}")
    return transaction_id


def cancel_pay(transaction_id: int) -> None:
    url = 'https://cs-bgu-wsep.herokuapp.com/'
    response = requests.post(url=url, data={"action_type": "handshake"})
    if str(response.content) != "b'OK'":
        raise Exception("Handshake went wrong")
    response = requests.post(url, data={"action_type": "cancel_pay", "transaction_id": transaction_id})
    suc_flag = int(response.content)
    if suc_flag == -1:
        raise Exception("Something went wrong with canceling the supply")