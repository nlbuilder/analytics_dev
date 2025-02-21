import sys, os
from dotenv import load_dotenv


# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)


import firebase_admin
from firebase_admin import credentials, auth
from pymongo import MongoClient, errors

from exception import CustomException


# initialize firebase app
cred = credentials.Certificate(
    os.path.join(parent_path, "firebase/serviceAccountKey.json")
)
firebase_admin.initialize_app(cred)


# connect to the mongodb client
from src.mongodb.mongodbClient import client


# get the database name from the .env file
load_dotenv()
business_database = os.getenv("BUSINESS_DATABASE")
business_info_collection = os.getenv("BUSINESS_INFO_COLLECTION")
business_staff_info_collection = os.getenv("BUSINESS_STAFF_INFO_COLLECTION")
business_service_info_collection = os.getenv("BUSINESS_SERVICE_INFO_COLLECTION")

customer_database = os.getenv("CUSTOMER_DATABASE")
customer_info_collection = os.getenv("CUSTOMER_INFO_COLLECTION")

# drop the collections in mongodb
business_db = client[business_database]
business_db[business_info_collection].drop()  # drop the business_info collection
business_db[
    business_staff_info_collection
].drop()  # drop the business_staff_info collection
business_db[
    business_service_info_collection
].drop()  # drop the business_services_info collection


customer_db = client[customer_database]
customer_db[customer_info_collection].drop()  # drop the customer_info collection


# delete all users in firebase
users_uid = []
for user in auth.list_users().iterate_all():
    users_uid.append(user.uid)

auth.delete_users(users_uid)

# delete csv files
path_to_business_csv = os.path.join(
    script_path, "simulation", "data", "business_info.csv"
)
path_to_business_staff_csv = os.path.join(
    script_path, "simulation", "data", "business_staff_info.csv"
)
path_to_save_customer_csv = os.path.join(
    script_path, "simulation", "data", "customer_info.csv"
)


os.remove(path_to_business_csv)
os.remove(path_to_business_staff_csv)
os.remove(path_to_save_customer_csv)
