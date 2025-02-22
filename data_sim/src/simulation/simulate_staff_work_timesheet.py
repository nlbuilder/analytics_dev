import os, sys, random
from dotenv import load_dotenv

# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)

from mongodbConnect.mongodbClient import client

from utils import (
    SimulateWorkTimeSheet,
    insert_data_to_mongodb,
    read_data_from_json,
    read_data_from_mongodb,
)


# read data from config json file
path_to_read_config_json = os.path.join(script_path, "config.json")
config_data = read_data_from_json(path_to_read_json=path_to_read_config_json)


# set things up
work_timesheets = []
min_number_of_work_timesheets = config_data["config"][
    "min_number_of_staff_work_timesheets"
]
max_number_of_work_timesheets = config_data["config"][
    "max_number_of_staff_work_timesheets"
]


# simulate work timesheets for each staff in each business
business_staff_data = read_data_from_mongodb(
    client=client, database_name="Business_DB", collection_name="business_staff_info"
)
business_ids = [staff["business_id"] for staff in business_staff_data]
business_staff_ids = [staff["business_staff_id"] for staff in business_staff_data]
business_staff_names = [
    f"{staff['first_name']} {staff['last_name']}" for staff in business_staff_data
]


# initialize the simulation classes
simulate_work_timesheet = SimulateWorkTimeSheet()


for business_id, business_staff_id in zip(
    business_ids,
    business_staff_ids,
):
    number_of_work_timesheets = random.randint(
        min_number_of_work_timesheets, max_number_of_work_timesheets
    )  # generate random number of work timesheets

    for _ in range(number_of_work_timesheets):
        work_timesheet_data = simulate_work_timesheet.generate_work_timesheet(
            business_id=business_id,
            business_staff_id=business_staff_id,
        )
        work_timesheets.append(work_timesheet_data)


# connect and insert data into Staff_work_timesheet_DB/daily_staff_work_timesheet
from src.mongodbConnect.mongodbClient import client

load_dotenv()
database = os.getenv("STAFF_WORK_TIMESHEET_DATABASE")
staff_work_timesheet_collection = os.getenv("DAILY_STAFF_WORK_TIMESHEET_COLLECTION")

# insert the generated businesses into the database
insert_data_to_mongodb(
    client=client,
    database_name=database,
    collection_name=staff_work_timesheet_collection,
    documents=work_timesheets,
    batch_size=1000,
)
