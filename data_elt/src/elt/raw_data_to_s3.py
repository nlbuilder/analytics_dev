import os, sys, random
from dotenv import load_dotenv

load_dotenv()


from src.mongodbConnect.mongodbClient import client
from src.utils import upload_mongo_to_s3

# get aws access key and secret key from the .env file
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")


# get the s3 bucket name from the .env file
s3_bucket_name = os.getenv("S3_BUCKET_NAME_RAW_DATA")

# ____________________________ BUSINESS DATABASE ____________________________
# get the database name from the .env file
# set things up for business info collection
database = os.getenv("BUSINESS_DATABASE")
collection = os.getenv("BUSINESS_INFO_COLLECTION")
business_staff_info_collection = os.getenv("BUSINESS_STAFF_INFO_COLLECTION")
s3_key = "business/business_info_collection.json"

# upload the business info collection to s3
upload_mongo_to_s3(
    client=client,
    database_name=database,
    collection_name=collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)

# set things up for business staff info collection
database = os.getenv("BUSINESS_DATABASE")
collection = os.getenv("BUSINESS_STAFF_INFO_COLLECTION")
s3_key = "business/business_staff_info_collection.json"

# upload the business staff info collection to s3
upload_mongo_to_s3(
    client=client,
    database_name=database,
    collection_name=collection,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    bucket_name=s3_bucket_name,
    s3_key=s3_key,
)

# ____________________________ BUSINESS SERVICE DATABASE ____________________________
# get the database name from the .env file
business_service_database = os.getenv("BUSINESS_SERVICE_DATABASE")
business_service_info_collection = os.getenv("BUSINESS_SERVICE_INFO_COLLECTION")

# ____________________________ CUSTOMER DATABASE ____________________________
# get the database name from the .env file
customer_database = os.getenv("CUSTOMER_DATABASE")
customer_info_collection = os.getenv("CUSTOMER_INFO_COLLECTION")

# ____________________________ APPOINTMENT DATABASE ____________________________
# get the database name from the .env file
appointment_database = os.getenv("APPOINTMENT_DATABASE")
appointment_info_collection = os.getenv("APPOINTMENT_INFO_COLLECTION")

# ____________________________ STAFF WORK TIMESHEET DATABASE ____________________________
# get the database name from the .env file
staff_work_timesheet_database = os.getenv("STAFF_WORK_TIMESHEET_DATABASE")
daily_staff_work_timesheet_collection = os.getenv(
    "DAILY_STAFF_WORK_TIMESHEET_COLLECTION"
)

# ____________________________ LOYALTY DATABASE ____________________________
# get the database name from the .env file
loyalty_program_database = os.getenv("LOYALTY_PROGRAM_DATABASE")
loyalty_card_collection = os.getenv("LOYALTY_CARD_COLLECTION")
