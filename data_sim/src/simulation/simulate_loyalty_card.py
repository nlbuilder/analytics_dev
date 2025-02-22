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
    SimulateLoyaltyCard,
    insert_data_to_mongodb,
    read_data_from_json,
    read_data_from_mongodb,
)


# read data from config json file
path_to_read_config_json = os.path.join(script_path, "config.json")
config_data = read_data_from_json(path_to_read_json=path_to_read_config_json)


# set things up
loyalty_cards = []
min_number_of_loyalty_cards = config_data["config"]["min_number_of_loyalty_cards"]
max_number_of_loyalty_cards = config_data["config"]["max_number_of_loyalty_cards"]


# simulate loyalty cards for each business
business_ids = read_data_from_mongodb(
    client=client, database_name="Business_DB", collection_name="business_info"
)
business_ids = [business["business_id"] for business in business_ids]

customer_ids = read_data_from_mongodb(
    client=client, database_name="Customer_DB", collection_name="customer_info"
)
customer_ids = [customer["customer_id"] for customer in customer_ids]


# initialize the simulation classes
simulate_loyalty_card = SimulateLoyaltyCard()


for business_id in business_ids:
    number_of_loyalty_cards = random.randint(
        min_number_of_loyalty_cards, max_number_of_loyalty_cards
    )  # generate random number of loyalty cards

    for _ in range(number_of_loyalty_cards):
        loyalty_card_data = simulate_loyalty_card.generate_loyalty_card(
            business_id=business_id,
            customer_id=random.choice(customer_ids),
        )
        loyalty_cards.append(loyalty_card_data)


# connect and insert data into Loyalty_program_DB/loyalty_card
from src.mongodbConnect.mongodbClient import client


load_dotenv()
database = os.getenv("LOYALTY_PROGRAM_DATABASE")
loyalty_card_collection = os.getenv("LOYALTY_CARD_COLLECTION")


# insert the generated businesses into the database
insert_data_to_mongodb(
    client=client,
    database_name=database,
    collection_name=loyalty_card_collection,
    documents=loyalty_cards,
    batch_size=1000,
)
