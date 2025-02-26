import os, sys, shutil
from io import StringIO

from pymongo import MongoClient
import boto3
import json
import pandas as pd

# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)


from exception import CustomException

# from src.mongodbConnect.mongodbClient import client


# def a function to upload data from MongoDB to S3
def upload_data_from_mongo_to_s3(
    client: MongoClient,
    database_name: str,
    collection_name: str,
    aws_access_key: str,
    aws_secret_key: str,
    bucket_name: str,
    s3_key: str,
) -> None:

    try:
        # Connect to MongoDB
        db = client[database_name]
        collection = db[collection_name]

        # Fetch data
        data = list(
            collection.find({}, {"_id": 0})
        )  # Exclude _id field to avoid BSON issues
        json_data = json.dumps(data, indent=4)

        # Upload to S3
        s3_client = boto3.client(
            "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json_data,
            ContentType="application/json",
        )

        print(f"Data uploaded successfully to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        raise CustomException(e, sys)


# def a function to read data from MongoDB
def read_data_from_mongodb(
    client: MongoClient, database_name: str, collection_name: str, query: dict = {}
) -> list:
    try:

        # get the database and collection
        db = client[database_name]
        collection = db[collection_name]

        # retrieve data from the collection
        documents = collection.find(query)

        # convert the cursor to a list
        return list(documents)

    except Exception as e:
        raise CustomException(e, sys)


# def a function to save a dataframe to a csv file
def save_dataframe_to_csv(
    df: pd.DataFrame, path_to_save_csv: str, file_name: str
) -> None:
    try:

        # check if the path_to_save_csv does not exist => create the directory
        if not os.path.exists(path_to_save_csv):
            os.makedirs(path_to_save_csv)

        # create the full path to save the csv file
        full_path_to_save_csv = os.path.join(path_to_save_csv, file_name)

        df.to_csv(full_path_to_save_csv, index=False)

    except Exception as e:
        raise CustomException(e, sys)


# def a function to upload dataframe to AWS S3
def upload_dataframe_to_s3(
    df: pd.DataFrame,
    aws_access_key: str,
    aws_secret_key: str,
    bucket_name: str,
    s3_key: str,
) -> None:
    try:

        # convert the dataframe to a csv string (in-memory)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # upload the csv string to S3
        s3_client = boto3.client(
            "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
        )
        s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())
        print(f"Successfully uploaded {s3_key} to {bucket_name}")

    except Exception as e:
        print(f"Failed to upload {s3_key} to {bucket_name}")
        raise CustomException(e, sys)


# def a function to clean local data
def clean_local_csv(path_to_remove: str) -> None:

    try:

        if os.path.exists(path_to_remove):
            with os.scandir(path_to_remove) as entries:
                for entry in entries:
                    if entry.is_dir():
                        shutil.rmtree(entry.path)
                    else:
                        os.remove(entry.path)
            print(f"All contents inside {path_to_remove} have been deleted.")
        else:
            print(f"Folder {path_to_remove} does not exist.")

    except Exception as e:
        raise CustomException(e, sys)


# def a function to remove data from MongoDB
def remove_data_from_mongodb(
    client: MongoClient, database_name: str, collection_name: str, query: dict = {}
) -> dict:

    try:
        # Get the database and collection
        db = client[database_name]
        collection = db[collection_name]

        # Delete matching documents
        result = collection.delete_many(query)

        # Return the number of deleted documents
        return {"deleted_count": result.deleted_count}

    except Exception as e:
        raise CustomException(e, sys)
