# WorkshopSEProject
Initilize system -
The initilization of the system done by json file, the default file is "init.json" but another file can be used by init_file flag.
The json file should contain these keys -
database -
admin - proporties of the administrator of the system.
external_systems - #TODO
commands - list of commands to get to a specific state. The supported commands are :
register(user_name,password,age)
login(user_name,password)
open_store(store_name,user_name)
assign_store_manager(user_name,new_store_manager_name,store_name)
assign_store_owner(user_name,new_store_owner_name,store_name)
add_new_product_to_store_inventory(user_name,product_details,store_name)
add_simple_discount(user_name,store,discount_name,discount_value)
add_product_to_cart(user_name,product_id,quantity,store_name)
purchase(user_name,payment_info,destination)
logout(user_name)
