import os, sys, json
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from collections import defaultdict
import boto3

# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)

from utils import (
    upload_dataframe_to_s3,
    clean_local_csv,
)
from marker import time_marker

time_marker = str(time_marker)


# ________________ GET THE ENVIRONMENT VARIABLES ________________ #
# get aws access key and secret key from the .env file
load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
database_name = os.getenv("APPOINTMENT_DATABASE")
collection_name = os.getenv("APPOINTMENT_INFO_COLLECTION")

# get the s3 bucket name from the .env file
s3_bucket_transformed_data_name = os.getenv("S3_BUCKET_NAME_TRANSFORMED_DATA")
aggregated_data_s3_key = f"{time_marker}/aggregated_data/aggregated_appointments.csv"

s3_bucket_raw_data_name = os.getenv("S3_BUCKET_NAME_RAW_DATA")
s3_key = f"{time_marker}/appointment/appointment_info_collection.json"


s3_client = boto3.client(
    "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
)

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ________________ READ RAWA DATA FROM S3 ________________ #
# fetch JSON file from S3
response = s3_client.get_object(Bucket=s3_bucket_raw_data_name, Key=s3_key)
json_data = response["Body"].read().decode("utf-8")

# convert JSON string to Python dictionary
appointment_data = json.loads(json_data)


# ________________ TRANSFORM THE DATA ________________ #
# prepare empty dictionaries to store the data
appointment_dataframes = defaultdict(list)
customer_aggregates = defaultdict(list)
hourly_aggregates = defaultdict(list)
weekday_aggregates = defaultdict(list)


# process each record
for record in appointment_data:
    business_id = record["business_id"]
    date_str = record["date"]
    time_str = record["time"]

    # convert to datetime object for easier manipulation
    datetime_obj = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

    # extract year, month, day, and hour
    year = datetime_obj.year
    month = datetime_obj.month
    day = datetime_obj.day
    weekday_index = datetime_obj.weekday()
    weekday = weekdays[weekday_index]

    # adjust hour based on minutes
    if datetime_obj.minute > 40:
        hour = datetime_obj.hour + 1
    else:
        hour = datetime_obj.hour

    # create a dictionary for the desired columns
    record_data = {
        "business_id": record["business_id"],
        "year": year,
        "month": month,
        "day": day,
        "weekday": weekday,
        "hour": hour,
        "customer_name": record["customer_name"],
        "customer_phone_number": record["customer_phone_number"],
        "number_of_customers": record["number_of_customers"],
    }

    # append the record data to the corresponding business_id list
    appointment_dataframes[business_id].append(record_data)

    # add data to the customer aggregation list
    customer_aggregates[business_id].append(
        {
            "customer_name": record["customer_name"],
            "customer_phone_number": record["customer_phone_number"],
            "appointment_count": 1,  # each record represents one appointment
        }
    )

    # add data to the hourly aggregation list
    hourly_aggregates[business_id].append(
        {
            "year": year,
            "month": month,
            "hour": hour,
            "number_of_customers": record["number_of_customers"],
        }
    )

    weekday_aggregates[business_id].append(
        {
            "year": year,
            "month": month,
            "day": day,
            "weekday": weekday,
            "number_of_customers": record["number_of_customers"],
        }
    )

# convert the lists to dataframes for each business_id
for business_id, records in appointment_dataframes.items():
    appointment_df = pd.DataFrame(records)

    grouped_df = appointment_df.groupby(["year", "month"])

    for (year, month), group in grouped_df:

        # upload the appointment data to S3
        appointment_s3_key = f"{time_marker}/by_businessId/{business_id}/appointment/appointment_counts/{year}/{month:02d}/{business_id}__{year}__{month:02d}__appointment_counts.csv"
        upload_dataframe_to_s3(
            group,
            aws_access_key,
            aws_secret_key,
            s3_bucket_transformed_data_name,
            appointment_s3_key,
        )

    # customer aggregate DataFrame
    customer_df = pd.DataFrame(customer_aggregates[business_id])

    # group by customer_name and customer_phone_number, summing the appointment_count
    customer_aggregate_df = customer_df.groupby(
        ["customer_name", "customer_phone_number"], as_index=False
    ).sum()

    # rename the columns for clarity
    customer_aggregate_df.rename(
        columns={"appointment_count": "total_booked_appointments"}, inplace=True
    )

    # upload the customer data to S3
    customer_s3_key = f"{time_marker}/by_businessId/{business_id}/customer_info/{year}/{month:02d}/{business_id}__{year}__{month:02d}__customer_info.csv"
    upload_dataframe_to_s3(
        customer_aggregate_df,
        aws_access_key,
        aws_secret_key,
        s3_bucket_transformed_data_name,
        customer_s3_key,
    )

    # hourly aggregate DataFrame
    hourly_df = pd.DataFrame(hourly_aggregates[business_id])

    # group by year, month, hour and sum the number_of_customers
    hourly_grouped_df = hourly_df.groupby(
        ["year", "month", "hour"], as_index=False
    ).sum()

    # split the data by year and month
    for (year, month), hourly_group in hourly_grouped_df.groupby(["year", "month"]):

        # upload the weekday data to S3
        hourly_s3_key = f"{time_marker}/by_businessId/{business_id}/appointment/hourly_aggregates/{year}/{month:02d}/{business_id}__{year}__{month:02d}__hourly_aggregates.csv"
        upload_dataframe_to_s3(
            hourly_group,
            aws_access_key,
            aws_secret_key,
            s3_bucket_transformed_data_name,
            hourly_s3_key,
        )

    # weekday aggregate DataFrame
    weekday_df = pd.DataFrame(weekday_aggregates[business_id])

    # group by year, month, day, weekday and sum the number_of_customers
    weekday_grouped_df = weekday_df.groupby(
        ["year", "month", "day", "weekday"], as_index=False
    ).sum()

    # split the data by year and month
    for (year, month), weekday_group in weekday_grouped_df.groupby(["year", "month"]):

        # upload the weekday data to S3
        weekday_s3_key = f"{time_marker}/by_businessId/{business_id}/appointment/weekday_aggregates/{year}/{month:02d}/{business_id}__{year}__{month:02d}__weekday_aggregates.csv"
        upload_dataframe_to_s3(
            weekday_group,
            aws_access_key,
            aws_secret_key,
            s3_bucket_transformed_data_name,
            weekday_s3_key,
        )

# ___________ CLEAN LOCAL CSV ___________ #
# remove everything under the folder data
path_to_remove = os.path.join(parent_path, "data")
clean_local_csv(path_to_remove)


# ___________ AGGREGATE APPOINTMENT DATA ___________ #
# make an aggregation of the appointment data (all business_ids)
# convert the appointment data to a DataFrame
appointment_data_df = pd.DataFrame(appointment_data)


# select only required columns
selected_columns = ["service_id", "service_name", "date", "time", "number_of_customers"]
df_aggregated = appointment_data_df[selected_columns]


upload_dataframe_to_s3(
    df_aggregated,
    aws_access_key,
    aws_secret_key,
    s3_bucket_transformed_data_name,
    aggregated_data_s3_key,
)
