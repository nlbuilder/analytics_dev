import os
from dotenv import load_dotenv

# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi


# load the specific .env file
load_dotenv()
MONGODB_CONNECTION_STRING_LOCAL = os.getenv("MONGODB_CONNECTION_URL_LOCAL")
MONGODB_CONNECTION_STRING_ONLINE = os.getenv("MONGODB_CONNECTION_URL_ONLINE")


# # Create a new client and connect to the server
# client = MongoClient(MONGODB_CONNECTION_STRING, server_api=ServerApi("1"))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command("ping")
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


print(MONGODB_CONNECTION_STRING_LOCAL)
print(MONGODB_CONNECTION_STRING_ONLINE)
