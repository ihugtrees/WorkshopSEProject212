import OnlineStore.src.data_layer.users_data as usersdb
import OnlineStore.src.service_layer.service as service

def initialize_system():
    service.register("admin", "admin")
    usersdb.get_user_by_name("admin").is_admin = True


initialize_system()
print(service.login("admin", "admin"))
