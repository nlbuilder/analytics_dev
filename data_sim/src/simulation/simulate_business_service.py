import os, sys, random
from dotenv import load_dotenv

# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)


from mongodb.mongodbClient import client

from utils import (
    SimulateService,
    insert_data_to_mongodb,
    read_data_from_mongodb,
    read_data_from_json,
)

# read data from config json file
path_to_read_config_json = os.path.join(script_path, "config.json")
config_data = read_data_from_json(path_to_read_json=path_to_read_config_json)


# set things up
services = []
service_preset = True  # True
# select a preset for services
selected_preset = "preset_service_for_nailsalon"


# set things up for using preset services
if service_preset:
    list_of_services = config_data[selected_preset]
    min_number_of_services = len(config_data[selected_preset][0])
    max_number_of_services = len(config_data[selected_preset][0])

# set things up for not using preset services
else:
    min_number_of_services = config_data["config"]["min_number_of_services"]
    max_number_of_services = config_data["config"]["max_number_of_services"]


# initialize the simulation classes
simulate_service = SimulateService()


load_dotenv()
database = os.getenv("BUSINESS_DATABASE")
business_servive_collection = os.getenv("BUSINESS_SERVICE_INFO_COLLECTION")


# simulate services for each business
business_data = read_data_from_mongodb(
    client=client, database_name="Business_DB", collection_name="business_info"
)
business_ids = [business["business_id"] for business in business_data]

for business_id in business_ids:
    number_of_service = random.randint(
        min_number_of_services, max_number_of_services
    )  # generate random number of services

    for _ in range(number_of_service):

        if service_preset:
            service_name = list(list_of_services[0].keys())[_]
            service_price = int(list(list_of_services[0].values())[_])
        else:
            service_name = None
            service_price = None

        service_data = simulate_service.generate_service(
            business_id=business_id,
            preset=service_preset,
            service_name=service_name,
            service_price=service_price,
        )

        services.append(service_data)


# insert the generated businesses into the database
insert_data_to_mongodb(
    client=client,
    database_name=database,
    collection_name=business_servive_collection,
    documents=services,
    batch_size=1000,
)
