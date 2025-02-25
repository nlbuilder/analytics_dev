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
    os.path.join(parent_path, "firebaseConfig/serviceAccountKey.json")
)
firebase_admin.initialize_app(cred)


# connect to the mongodb client
from src.mongodbConnect.mongodbClient import client


# get the database name from the .env file
load_dotenv()
business_database = os.getenv("BUSINESS_DATABASE")
business_info_collection = os.getenv("BUSINESS_INFO_COLLECTION")
business_staff_info_collection = os.getenv("BUSINESS_STAFF_INFO_COLLECTION")
# business_service_info_collection = os.getenv("BUSINESS_SERVICE_INFO_COLLECTION")

business_service_database = os.getenv("BUSINESS_SERVICE_DATABASE")
business_service_info_collection = os.getenv("BUSINESS_SERVICE_INFO_COLLECTION")


customer_database = os.getenv("CUSTOMER_DATABASE")
customer_info_collection = os.getenv("CUSTOMER_INFO_COLLECTION")

appointment_database = os.getenv("APPOINTMENT_DATABASE")
appointment_info_collection = os.getenv("APPOINTMENT_INFO_COLLECTION")

staff_work_timesheet_database = os.getenv("STAFF_WORK_TIMESHEET_DATABASE")
staff_work_timesheet_collection = os.getenv("DAILY_STAFF_WORK_TIMESHEET_COLLECTION")

loyalty_program_database = os.getenv("LOYALTY_PROGRAM_DATABASE")
loyalty_program_collection = os.getenv("LOYALTY_CARD_COLLECTION")

# drop the collections in mongodb
business_db = client[business_database]
business_db[business_info_collection].drop()  # drop the business_info collection
business_db[
    business_staff_info_collection
].drop()  # drop the business_staff_info collection


business_service_db = client["Business_service_DB"]
business_service_db[
    business_service_info_collection
].drop()  # drop the business_services_info collection


customer_db = client[customer_database]
customer_db[customer_info_collection].drop()  # drop the customer_info collection


appointment_db = client[appointment_database]
appointment_db[
    appointment_info_collection
].drop()  # drop the appointment_info collection


staff_work_timesheet_db = client[staff_work_timesheet_database]
staff_work_timesheet_db[
    staff_work_timesheet_collection
].drop()  # drop the daily_staff_work_timesheet collection


loyalty_program_db = client[loyalty_program_database]
loyalty_program_db[
    loyalty_program_collection
].drop()  # drop the loyalty_program collection


# delete all users in firebase
users_uid = []
for user in auth.list_users().iterate_all():
    users_uid.append(user.uid)

auth.delete_users(users_uid)

# delete csv files
# path_to_business_csv = os.path.join(
#     script_path, "simulation", "data", "business_info.csv"
# )
# path_to_business_staff_csv = os.path.join(
#     script_path, "simulation", "data", "business_staff_info.csv"
# )
# path_to_save_customer_csv = os.path.join(
#     script_path, "simulation", "data", "customer_info.csv"
# )


# os.remove(path_to_business_csv)
# os.remove(path_to_business_staff_csv)
# os.remove(path_to_save_customer_csv)
