import os, sys

from pymongo import MongoClient
import boto3
import json


from exception import CustomException
from src.mongodbConnect.mongodbClient import client


# def a function to upload data from MongoDB to S3
def upload_mongo_to_s3(
    client: MongoClient,
    database_name: str,
    collection_name: str,
    aws_access_key: str,
    aws_secret_key: str,
    bucket_name: str,
    s3_key: str,
    batch_size: int = 1000,
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
        s3 = boto3.client(
            "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
        )
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json_data,
            ContentType="application/json",
        )

        print(f"Data uploaded successfully to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        raise CustomException(e, sys)
