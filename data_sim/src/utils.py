import json
import random
import sys, os, csv
from faker import Faker
from datetime import datetime, timedelta


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


# def a class to generate business
class SimulateBusiness:
    def __init__(self, seed=0):
        self.fake = Faker()
        # self.fake.seed_instance(seed)  # seed the faker instance * IMPORTANT *

    def generate_business(self, path_to_save_csv: str):
        try:

            business = {
                "name": self.fake.company(),
                "address_line1": self.fake.street_address(),
                "address_line2": self.fake.secondary_address(),
                "city": self.fake.city(),
                "state": self.fake.state(),
                "zip": self.fake.zipcode(),
                "country": self.fake.country(),
                "phone_number": self.fake.phone_number(),
                "email": self.fake.email(),
                "password": self.fake.password(),  # generate a random password to sign up with firebase
                "logo_url": self.fake.image_url(),
                "description": self.fake.bs(),
                "manager_name": self.fake.name(),
            }

            user = auth.create_user(
                email=business["email"], password=business["password"]
            )
            uid = user.uid

            # check if the file exists to determine if the header needs to be written
            file_exists = os.path.isfile(path_to_save_csv)

            with open(path_to_save_csv, mode="a", newline="") as file:
                writer = csv.writer(file)

                # write header if the file does not exist
                if not file_exists:
                    writer.writerow(["type", "email", "password", "uid"])

                writer.writerow(
                    ["business", business["email"], business["password"], uid]
                )

            business["business_id"] = uid

            return business

        except Exception as e:
            raise CustomException(e, sys)


# def a class to generate staff
class SimulateStaff:
    def __init__(self):
        self.fake = Faker()
        # self.fake.seed_instance(seed)  # seed the faker instance * IMPORTANT *

    def generate_staff(self, business_id: str, path_to_save_csv: str):
        try:

            business_staff = {
                "business_id": business_id,
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "address_line1": self.fake.street_address(),
                "address_line2": self.fake.secondary_address(),
                "city": self.fake.city(),
                "state": self.fake.state(),
                "zip": self.fake.zipcode(),
                "country": self.fake.country(),
                "phone_number": self.fake.phone_number(),
                "email": self.fake.email(),
                "password": self.fake.password(),  # generate a random password to sign up with firebase
                "profile_picture_url": self.fake.image_url(),
                "role": "staff",
            }

            user = auth.create_user(
                email=business_staff["email"], password=business_staff["password"]
            )
            uid = user.uid

            # check if the file exists to determine if the header needs to be written
            file_exists = os.path.isfile(path_to_save_csv)

            with open(path_to_save_csv, mode="a", newline="") as file:
                writer = csv.writer(file)

                # write header if the file does not exist
                if not file_exists:
                    writer.writerow(
                        [
                            "type",
                            "email",
                            "password",
                            "business_id",
                            "business_staff_id",
                        ]
                    )

                writer.writerow(
                    [
                        "business_staff",
                        business_staff["email"],
                        business_staff["password"],
                        business_staff["business_id"],
                        uid,
                    ]
                )

            business_staff["business_staff_id"] = uid

            return business_staff

        except Exception as e:
            raise CustomException(e, sys)


# def a class to generate services
class SimulateService:
    def __init__(
        self,
    ):
        self.fake = Faker()
        # self.fake.seed_instance(seed)  # seed the faker instance * IMPORTANT *

    def generate_service(
        self,
        business_id: str,
        preset: bool = False,
        service_name: str = None,
        service_price: int = None,
    ):
        try:

            preset = preset

            if preset:
                if service_name is None:
                    raise ValueError(
                        "service name must be provided when preset is True."
                    )
                elif service_price is None:
                    raise ValueError(
                        "service price must be provided when preset is True."
                    )

                service_name = service_name
                service_price = service_price
            else:
                service_name = self.fake.catch_phrase()
                service_price = self.fake.random_int(min=10, max=100, step=5)

            business_service = {
                "business_id": business_id,
                "service_id": self.fake.uuid4(),
                "service_name": service_name,
                "photo_url": self.fake.image_url(),
                "description": "super cool service",
                "price": service_price,
                "notes": "how cool is this service",
            }

            return business_service

        except Exception as e:
            raise CustomException(e, sys)


#  def a class to generate appointments
class SimulateAppointment:
    def __init__(self, min_number_of_customers=1, max_number_of_customers=10):
        self.fake = Faker()
        # self.fake.seed_instance(seed)  # seed the faker instance * IMPORTANT *
        self.min_number_of_customers = min_number_of_customers
        self.max_number_of_customers = max_number_of_customers

    def generate_appointment(
        self,
        business_id: str,
        service_id: str,
        service_name: str,
        customer_id: str,
        customer_phone_number: str,
        customer_name: str,
    ):
        try:

            # simulate a date using the faker library
            date = self.fake.date_this_year()
            date_formatted = date.strftime("%Y-%m-%d")

            # simulate a random time between 9 AM and 6 PM
            start_time = datetime.strptime("09:00:00", "%H:%M:%S")
            end_time = datetime.strptime("18:00:00", "%H:%M:%S")

            # Generate a random number of seconds between 9 AM and 6 PM
            random_seconds = random.randint(
                0, int((end_time - start_time).total_seconds())
            )

            # Add random seconds to the start time
            random_time = start_time + timedelta(seconds=random_seconds)

            # Round the time to the nearest 5 minutes
            rounded_minute = round(random_time.minute / 5) * 5

            # If rounding produces 60 minutes, increment the hour and set minute to 0
            if rounded_minute == 60:
                random_time = random_time + timedelta(hours=1)
                rounded_minute = 0

            # Set the new time with rounded minutes
            random_time = random_time.replace(minute=rounded_minute, second=0)

            time_formatted = random_time.strftime("%H:%M:%S")

            # # simulate a random time using the faker library, no constrait
            # random_time = self.fake.time()

            # # round the time to the nearest 5 minutes
            # time_obj = datetime.strptime(random_time, "%H:%M:%S")
            # rounded_minute = round(time_obj.minute / 5) * 5

            # # if rounding produces 60 minutes, increment the hour and set minute to 0
            # if rounded_minute == 60:
            #     time_obj = time_obj + timedelta(hours=1)
            #     rounded_minute = 0

            # time_obj = time_obj.replace(minute=rounded_minute, second=0)
            # time_formatted = time_obj.strftime("%H:%M:%S")

            appointment = {
                "appointment_id": f"{business_id}--{self.fake.uuid4()}",
                "business_id": business_id,
                "customer_id": customer_id,
                "customer_name": customer_name,
                "service_id": service_id,
                "date": date_formatted,
                "time": time_formatted,
                "number_of_customers": self.fake.random_int(
                    min=self.min_number_of_customers, max=self.max_number_of_customers
                ),  # random number of customers
                "service_name": service_name,
                "customer_phone_number": customer_phone_number,
                "status": self.fake.random_element(
                    elements=("waiting", "completed", "ongoing")
                ),
                "notes": "how awesome is this service and the staff, love it",
            }

            return appointment

        except Exception as e:
            raise CustomException(e, sys)


# def a class to generate daily staff work timesheet
class SimulateWorkTimeSheet:
    def __init__(self):
        self.fake = Faker()
        # self.fake.seed_instance(seed)  # seed the faker instance * IMPORTANT *

    def generate_work_timesheet(
        self,
        business_id: str,
        business_staff_id: str,
    ):
        try:

            date = self.fake.date_this_year()
            date_formatted = date.strftime("%Y-%m-%d")

            week_start = date - timedelta(
                days=date.weekday()
            )  # get the start date of the week

            week_start_formatted = week_start.strftime("%Y-%m-%d")

            # generate a random check-in time and make sure it is before the latest check-in time
            # set the time limit for the check-in (6 PM)
            latest_check_in_time = datetime.strptime("18:00:00", "%H:%M:%S").time()
            check_in_time = self.fake.time()
            while (
                datetime.strptime(check_in_time, "%H:%M:%S").time()
                > latest_check_in_time
            ):
                check_in_time = self.fake.time()
            # convert check-in time to datetime object
            check_in = datetime.strptime(check_in_time, "%H:%M:%S")

            # set the maximum duration of work (10 hours)
            max_duration = timedelta(hours=10)

            # generate a random check-out time and make sure it is after the check-in time
            # also make sure the total hours of work is less than the maximum duration
            check_out_time = self.fake.time_object()  # generate a random time object
            while True:
                check_out = datetime.combine(check_in.date(), check_out_time)
                if check_out > check_in and (check_out - check_in) < max_duration:
                    break
                check_out_time = self.fake.time_object()

            # convert check-out time to datetime object
            check_out = datetime.strptime(
                check_out_time.strftime("%H:%M:%S"), "%H:%M:%S"
            )

            # calculate total hours of work
            total_hours_of_work = (check_out - check_in).seconds / 3600

            work_timesheet = {
                "business_id": business_id,
                "business_staff_id": business_staff_id,
                "week_start": week_start_formatted,
                "date": date_formatted,
                "check_in_time": check_in_time,
                "check_out_time": check_out_time.strftime(
                    "%H:%M"
                ),  # format time as string
                "total_hours_of_work": round(
                    total_hours_of_work, 2
                ),  # round to 2 decimal places
                "manager_approval": True,
            }

            return work_timesheet

        except Exception as e:
            raise CustomException(e, sys)


# def a class for loyalty card
class SimulateLoyaltyCard:
    def __init__(self):
        self.fake = Faker()
        # self.fake.seed_instance(seed)  # seed the faker instance * IMPORTANT *

    def generate_loyalty_card(
        self,
        business_id: str,
        customer_id: str,
    ):
        try:

            date = self.fake.date_this_year()
            date_formatted = date.strftime("%Y-%m-%d")

            number_of_reward_points = self.fake.random_int(min=0, max=10)
            if number_of_reward_points == 10:
                number_of_redeemable_points = 1
            else:
                number_of_redeemable_points = 0

            loyalty_card = {
                "business_id": business_id,
                "customer_id": customer_id,
                "loyalty_card_id": self.fake.uuid4(),
                "number_of_reward_points": number_of_reward_points,
                "number_of_redeemable_points": number_of_redeemable_points,
                "number_of_redemptions": self.fake.random_int(min=0, max=10),
                "last_updated": date_formatted,
            }

            return loyalty_card

        except Exception as e:
            raise CustomException(e, sys)


# def a class to generate customer
class SimulateCustomer:
    def __init__(self):
        self.fake = Faker()
        # self.fake.seed_instance(seed)  # seed the faker instance * IMPORTANT *

    def generate_customer(self, path_to_save_csv: str):
        try:

            DOB = self.fake.date_of_birth()
            DOB_formatted = DOB.strftime("%Y-%m-%d")

            customer = {
                "customer_id": self.fake.uuid4(),
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "DOB": DOB_formatted,
                "phone_number": self.fake.phone_number(),
                "email": self.fake.email(),
                "password": self.fake.password(),
                "profile_picture_url": self.fake.image_url(),
                "address_line1": self.fake.street_address(),
                "address_line2": self.fake.secondary_address(),
                "city": self.fake.city(),
                "state": self.fake.state(),
                "zip": self.fake.zipcode(),
                "country": self.fake.country(),
            }

            # check if the file exists to determine if the header needs to be written
            file_exists = os.path.isfile(path_to_save_csv)

            with open(path_to_save_csv, mode="a", newline="") as file:
                writer = csv.writer(file)

                # write header if the file does not exist
                if not file_exists:
                    writer.writerow(
                        [
                            "type",
                            "email",
                            "password",
                            "uid",
                        ]
                    )

                writer.writerow(
                    [
                        "customer",
                        customer["email"],
                        customer["password"],
                        customer["customer_id"],
                    ]
                )

            return customer

        except Exception as e:
            raise CustomException(e, sys)


def insert_data_to_mongodb(
    client: MongoClient,
    database_name: str,
    collection_name: str,
    documents: list,
    batch_size: int,
) -> None:

    try:
        # initialize MongoDB client
        db = client[database_name]
        collection = db[collection_name]

        if len(documents) <= batch_size:
            # if the number of documents is less than or equal to batch_size, insert them all at once
            collection.insert_many(documents, ordered=False)
            print("Inserted all documents at once")
        else:
            # else, insert documents in batches
            for i in range(0, len(documents), batch_size):
                batch = documents[i : i + batch_size]
                collection.insert_many(batch, ordered=False)
                print(f"Inserted batch {i // batch_size + 1}")

    except errors.BulkWriteError as e:
        print("BulkWriteError:", e.details)


# def a function to read business ids from a csv file
def read_ids(path_to_read_csv: str):
    ids = []

    try:

        with open(path_to_read_csv, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row.get("uid")
                if id:
                    ids.append(id)

        return ids

    except Exception as e:
        raise CustomException(e, sys)


# def a function to read business_staff_info.csv
def read_business_staff_info(path_to_read_csv: str):
    business_ids = []
    business_staff_ids = []
    first_names = []
    last_names = []

    try:

        with open(path_to_read_csv, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                business_id = row.get("business_id")
                if business_id:
                    business_ids.append(business_id)

                business_staff_id = row.get("business_staff_id")
                if business_staff_id:
                    business_staff_ids.append(business_staff_id)

                first_name = row.get("first_name")
                if first_name:
                    first_names.append(first_name)

                last_name = row.get("last_name")
                if last_name:
                    last_names.append(last_name)

        return business_ids, business_staff_ids, first_names, last_names

    except Exception as e:
        raise CustomException(e, sys)


# def a function to read customer_info.csv
def read_customer_info(path_to_read_csv: str):
    ids = []
    phone_numbers = []
    first_names = []

    try:

        with open(path_to_read_csv, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row.get("uid")
                if id:
                    ids.append(id)

                phone_number = row.get("phone_number")
                if phone_number:
                    phone_numbers.append(phone_number)

                first_name = row.get("first_name")
                if first_name:
                    first_names.append(first_name)

        return ids, phone_numbers, first_names

    except Exception as e:
        raise CustomException(e, sys)


# def a function to read service_info.csv
def read_service_info(path_to_read_csv: str):
    service_ids = []
    service_names = []
    business_ids = []

    try:

        with open(path_to_read_csv, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                service_id = row.get("service_id")
                if service_id:
                    service_ids.append(service_id)

                service_name = row.get("service_name")
                if service_name:
                    service_names.append(service_name)

                business_id = row.get("business_id")
                if business_id:
                    business_ids.append(business_id)

        return service_ids, service_names, business_ids

    except Exception as e:
        raise CustomException(e, sys)


# def a function to read data from MongoDB
def read_data_from_mongodb(
    client: MongoClient, database_name: str, collection_name: str, query: dict = {}
):
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


# def a function to read data from a json file
def read_data_from_json(path_to_read_json: str):
    try:

        with open(path_to_read_json, "r") as file:
            data = json.load(file)

        return data

    except Exception as e:
        raise CustomException(e, sys)
