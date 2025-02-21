import os, sys, random
from dotenv import load_dotenv


# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)


from utils import (
    SimulateBusiness,
    SimulateStaff,
    insert_data_to_mongodb,
    read_data_from_json,
)


# read data from config json file
path_to_read_config_json = os.path.join(script_path, "config.json")
config_data = read_data_from_json(path_to_read_json=path_to_read_config_json)


path_to_save_business_csv = "./data/business_info.csv"
path_to_save_business_staff_csv = "./data/business_staff_info.csv"

# split the path to get the directory path
dir_to_save_business_csv = os.path.split(path_to_save_business_csv)[0]
# check if the directory exists, if not create it
if not os.path.exists(dir_to_save_business_csv):
    os.makedirs(dir_to_save_business_csv)


# set things up
businesses = []
business_staffs = []
number_of_business = config_data["config"]["number_of_businesses"]
min_number_of_staff = config_data["config"]["min_number_of_staffs"]
max_number_of_staff = config_data["config"]["max_number_of_staffs"]


# initialize the simulation classes
simulate_business = SimulateBusiness()
simulate_staff = SimulateStaff()


# generate businesses
for i in range(number_of_business):
    business_data = simulate_business.generate_business(
        path_to_save_csv=path_to_save_business_csv
    )
    businesses.append(business_data)

# generate staffs for each business
for i in range(number_of_business):
    number_of_staff = random.randint(
        min_number_of_staff, max_number_of_staff
    )  # generate random number of staffs

    for _ in range(number_of_staff):
        business_staff_data = simulate_staff.generate_staff(
            business_id=businesses[i]["business_id"],
            path_to_save_csv=path_to_save_business_staff_csv,
        )
        business_staffs.append(business_staff_data)


# remove password from businesses
for business in businesses:
    business.pop("password")

# connect and insert data into Business_DB/business_info and Business_DB/business_staff_info
from src.mongodb.mongodbClient import client


# get the database name from the .env file
load_dotenv()
database = os.getenv("BUSINESS_DATABASE")
business_info_collection = os.getenv("BUSINESS_INFO_COLLECTION")
business_staff_info_collection = os.getenv("BUSINESS_STAFF_INFO_COLLECTION")


# insert the generated businesses into the database
insert_data_to_mongodb(
    client=client,
    database_name=database,
    collection_name=business_info_collection,
    documents=businesses,
    batch_size=1000,
)

# insert the generated business staffs into the database
insert_data_to_mongodb(
    client=client,
    database_name=database,
    collection_name=business_staff_info_collection,
    documents=business_staffs,
    batch_size=1000,
)
