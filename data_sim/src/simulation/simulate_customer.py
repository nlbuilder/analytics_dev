import os, sys
from dotenv import load_dotenv


# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)

from utils import SimulateCustomer, insert_data_to_mongodb, read_data_from_json


# read data from config json file
path_to_read_config_json = os.path.join(script_path, "config.json")
config_data = read_data_from_json(path_to_read_json=path_to_read_config_json)


# set things up
customers = []
number_of_customers = config_data["config"]["number_of_customers"]
path_to_save_customer_csv = os.path.join("./data/customer_info.csv")


# initialize the simulation classes
simulate_customer = SimulateCustomer()


# generate customers
for i in range(number_of_customers):
    customer_data = simulate_customer.generate_customer(
        path_to_save_csv=path_to_save_customer_csv
    )
    customers.append(customer_data)

# connect and insert data into Customer_DB/customer_info
from src.mongodbConnect.mongodbClient import client


load_dotenv()
database = os.getenv("CUSTOMER_DATABASE")
customer_info_collection = os.getenv("CUSTOMER_INFO_COLLECTION")


# insert the generated customers into the database
insert_data_to_mongodb(
    client=client,
    database_name=database,
    collection_name=customer_info_collection,
    documents=customers,
    batch_size=1000,
)
