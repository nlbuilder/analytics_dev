import os, sys
from dotenv import load_dotenv


# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)

from mongodbConnect.mongodbClient import client
from utils import remove_data_from_mongodb
from marker import time_marker


time_marker = str(time_marker)


# ____________________________ BUSINESS DATABASE ____________________________
# get the database name from the .env file
business_database = os.getenv("BUSINESS_DATABASE")
business_info_collection = os.getenv("BUSINESS_INFO_COLLECTION")
remove_data_from_mongodb(client, business_database, business_info_collection)


# ____________________________ BUSINESS SERVICE DATABASE ____________________________
# get the database name from the .env file
business_service_database = os.getenv("BUSINESS_SERVICE_DATABASE")
business_service_info_collection = os.getenv("BUSINESS_SERVICE_INFO_COLLECTION")
remove_data_from_mongodb(
    client, business_service_database, business_service_info_collection
)


# ____________________________ CUSTOMER DATABASE ____________________________
# get the database name from the .env file
customer_database = os.getenv("CUSTOMER_DATABASE")
customer_info_collection = os.getenv("CUSTOMER_INFO_COLLECTION")
remove_data_from_mongodb(client, customer_database, customer_info_collection)


# ____________________________ APPOINTMENT DATABASE ____________________________
# get the database name from the .env file
appointment_database = os.getenv("APPOINTMENT_DATABASE")
appointment_info_collection = os.getenv("APPOINTMENT_INFO_COLLECTION")
remove_data_from_mongodb(client, appointment_database, appointment_info_collection)


# ____________________________ STAFF WORK TIMESHEET DATABASE ____________________________
# get the database name from the .env file
staff_work_timesheet_database = os.getenv("STAFF_WORK_TIMESHEET_DATABASE")
daily_staff_work_timesheet_collection = os.getenv(
    "DAILY_STAFF_WORK_TIMESHEET_COLLECTION"
)
remove_data_from_mongodb(
    client, staff_work_timesheet_database, daily_staff_work_timesheet_collection
)


# ____________________________ LOYALTY DATABASE ____________________________
# get the database name from the .env file
loyalty_program_database = os.getenv("LOYALTY_PROGRAM_DATABASE")
loyalty_card_collection = os.getenv("LOYALTY_CARD_COLLECTION")
remove_data_from_mongodb(client, loyalty_program_database, loyalty_card_collection)
