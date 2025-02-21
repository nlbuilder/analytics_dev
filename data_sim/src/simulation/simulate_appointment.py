import os, sys, random

# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)


from mongodb.mongodbClient import client

from utils import (
    SimulateAppointment,
    insert_data_to_mongodb,
    read_data_from_json,
    read_data_from_mongodb,
)


# read data from config json file
path_to_read_config_json = os.path.join(script_path, "config.json")
config_data = read_data_from_json(path_to_read_json=path_to_read_config_json)


# set things up
appointments = []
min_number_of_appointments = config_data["config"]["min_number_of_appointments"]
max_number_of_appointments = config_data["config"]["max_number_of_appointments"]


# simulate appointments for each business
business_ids = read_data_from_mongodb(
    client=client, database_name="Business_DB", collection_name="business_info"
)
business_ids = [business["business_id"] for business in business_ids]


customer_data = read_data_from_mongodb(
    client=client, database_name="Customer_DB", collection_name="customer_info"
)
customer_ids = [customer["customer_id"] for customer in customer_data]
customer_phone_numbers = [customer["phone_number"] for customer in customer_data]
customer_names = [
    f"{customer['first_name']} {customer['last_name']}" for customer in customer_data
]


service_data = read_data_from_mongodb(
    client=client,
    database_name="Business_service_DB",
    collection_name="business_service_info",
)
service_ids = [service["service_id"] for service in service_data]
service_names = [service["service_name"] for service in service_data]


# initialize the simulation classes
simulate_appointment = SimulateAppointment()


for business_id in business_ids:
    number_of_appointments = random.randint(
        min_number_of_appointments, max_number_of_appointments
    )  # generate random number of appointments

    # filter services specific to the current business_id
    business_service_options = [
        (service_id, service_name)
        for service_id, service_name, business_service_id in zip(
            service_ids, service_names, business_ids
        )
        if business_service_id == business_id
    ]

    for _ in range(number_of_appointments):
        # randomly select a customer
        chosen_customer_index = random.randint(0, len(customer_ids) - 1)
        customer_id = customer_ids[chosen_customer_index]
        customer_phone_number = customer_phone_numbers[chosen_customer_index]
        customer_name = customer_names[chosen_customer_index]

        # randomly select a service from the business-specific services
        chosen_service_id, chosen_service_name = random.choice(business_service_options)

        appointment_data = simulate_appointment.generate_appointment(
            business_id=business_id,
            customer_id=customer_id,
            customer_phone_number=customer_phone_number,
            customer_name=customer_name,
            service_id=chosen_service_id,
            service_name=chosen_service_name,
        )

        appointments.append(appointment_data)


# connect and insert data into Business_DB/business_info and Business_DB/business_staff_info
DATABASE_NAME = "Appointment_DB"

# insert the generated businesses into the database
insert_data_to_mongodb(
    client=client,
    database_name=DATABASE_NAME,
    collection_name="appointment_info",
    documents=appointments,
    batch_size=1000,
)
