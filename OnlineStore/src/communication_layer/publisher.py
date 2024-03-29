import flask
from flask_socketio import send, emit

from OnlineStore.src.data_layer import users_data
import OnlineStore.src.domain_layer.domain_handler as domain_handler
import OnlineStore.src.data_layer.users_data as user_data_handler

topics = dict()


def send_message(message, to, event):
    lock = domain_handler.auth.check_logged_and_take_lock(to)
    if lock == None:
        user_data_handler.add_message(to, message, event)
    else:
        try:
            user_data_handler.add_message_to_history(to, message, event)
            socket_io = flask.current_app.extensions['socketio']
        except Exception as e:
            lock.release()
            return
        socket_io.emit(event=event, room=to, data=message)
        lock.release()


def send_message_to_store_employees(message, store_name, event):
    for owner in topics[store_name]:
        send_message(message, owner, event)


def send_remove_employee_msg(message, to):
    send_message(message, to, "remove employee")


def send_messages(username):
    try:
        messages = users_data.pop_user_messages(username)
        socket_io = flask.current_app.extensions['socketio']
        for message_dict in messages:
            send_message(message=message_dict["message"],to=username,event=message_dict["event"])
            #socket_io.emit(data=message_dict["message"], room=username, event=message_dict["event"])
    except Exception as e:
        print(e.args[0])
        return


def subscribe(username, store_name):
    if store_name not in topics:
        topics[store_name] = list()
    topics[store_name].append(username)


def unsubscribe(username, store_name):
    if store_name not in topics:
        raise Exception("Unsubscribe fail")
    topics[store_name].remove(username)


def delete_store(store_name) -> None:
    topics.pop(store_name)
