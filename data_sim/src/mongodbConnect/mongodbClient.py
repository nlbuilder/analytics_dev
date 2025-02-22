import os
from dotenv import load_dotenv
import certifi  # to handle SSL certificate verification in order to connect to MongoDB Atlas

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# load the specific .env file
load_dotenv()
MONGODB_CONNECTION_STRING_LOCAL = os.getenv("MONGODB_CONNECTION_URL_LOCAL")
MONGODB_CONNECTION_STRING_PRODUCTION = os.getenv("MONGODB_CONNECTION_URL_PRODUCTION")

# Create a new client and connect to the server
# chosen_connection_string = MONGODB_CONNECTION_STRING_LOCAL
chosen_connection_string = MONGODB_CONNECTION_STRING_PRODUCTION

if chosen_connection_string == MONGODB_CONNECTION_STRING_PRODUCTION:
    client = MongoClient(
        MONGODB_CONNECTION_STRING_PRODUCTION,
        server_api=ServerApi("1"),
        tlsCAFile=certifi.where(),  # to handle SSL certificate verification in order to connect to MongoDB Atlas
    )
else:
    client = MongoClient(
        MONGODB_CONNECTION_STRING_LOCAL,
        server_api=ServerApi("1"),
    )


# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
