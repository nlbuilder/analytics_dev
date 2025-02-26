import os, sys
from dotenv import load_dotenv


# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)


from mongodbConnect.mongodbClient import client
from utils import upload_data_from_mongo_to_s3
from marker import time_marker


time_marker = str(time_marker)


# get aws access key and secret key from the .env file
load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")


# get the s3 bucket name from the .env file
s3_bucket_name = os.getenv("S3_BUCKET_NAME_RAW_DATA")


# ____________________________ BUSINESS DATABASE ____________________________
# get the database name from the .env file
# set things up for business info collection
business_database = os.getenv("BUSINESS_DATABASE")
business_info_collection = os.getenv("BUSINESS_INFO_COLLECTION")
s3_key = f"{time_marker}/business/business_info_collection.json"

# upload the business info collection to s3
upload_data_from_mongo_to_s3(
    client=client,
    database_name=business_database,
    collection_name=business_info_collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)

# set things up for business staff info collection
business_database = os.getenv("BUSINESS_DATABASE")
business_staff_info_collection = os.getenv("BUSINESS_STAFF_INFO_COLLECTION")
s3_key = f"{time_marker}/business/business_staff_info_collection.json"

# upload the business staff info collection to s3
upload_data_from_mongo_to_s3(
    client=client,
    database_name=business_database,
    collection_name=business_staff_info_collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)


# ____________________________ BUSINESS SERVICE DATABASE ____________________________
# get the database name from the .env file
business_service_database = os.getenv("BUSINESS_SERVICE_DATABASE")
business_service_info_collection = os.getenv("BUSINESS_SERVICE_INFO_COLLECTION")
s3_key = f"{time_marker}/business_service/business_service_info_collection.json"

upload_data_from_mongo_to_s3(
    client=client,
    database_name=business_service_database,
    collection_name=business_service_info_collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)


# ____________________________ CUSTOMER DATABASE ____________________________
# get the database name from the .env file
customer_database = os.getenv("CUSTOMER_DATABASE")
customer_info_collection = os.getenv("CUSTOMER_INFO_COLLECTION")
s3_key = f"{time_marker}/customer/customer_info_collection.json"

upload_data_from_mongo_to_s3(
    client=client,
    database_name=customer_database,
    collection_name=customer_info_collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)


# ____________________________ APPOINTMENT DATABASE ____________________________
# get the database name from the .env file
appointment_database = os.getenv("APPOINTMENT_DATABASE")
appointment_info_collection = os.getenv("APPOINTMENT_INFO_COLLECTION")
s3_key = f"{time_marker}/appointment/appointment_info_collection.json"

upload_data_from_mongo_to_s3(
    client=client,
    database_name=appointment_database,
    collection_name=appointment_info_collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)


# ____________________________ STAFF WORK TIMESHEET DATABASE ____________________________
# get the database name from the .env file
staff_work_timesheet_database = os.getenv("STAFF_WORK_TIMESHEET_DATABASE")
daily_staff_work_timesheet_collection = os.getenv(
    "DAILY_STAFF_WORK_TIMESHEET_COLLECTION"
)
s3_key = (
    f"{time_marker}/staff_work_timesheet/daily_staff_work_timesheet_collection.json"
)


upload_data_from_mongo_to_s3(
    client=client,
    database_name=staff_work_timesheet_database,
    collection_name=daily_staff_work_timesheet_collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)


# ____________________________ LOYALTY DATABASE ____________________________
# get the database name from the .env file
loyalty_program_database = os.getenv("LOYALTY_PROGRAM_DATABASE")
loyalty_card_collection = os.getenv("LOYALTY_CARD_COLLECTION")
s3_key = f"{time_marker}/loyalty_program/loyalty_card_collection.json"

upload_data_from_mongo_to_s3(
    client=client,
    database_name=loyalty_program_database,
    collection_name=loyalty_card_collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)
