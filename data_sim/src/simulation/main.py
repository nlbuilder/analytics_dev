import subprocess

# run simulate_business.py
print("Running simulate_business.py")
subprocess.run(["python", "simulate_business.py"], check=True)

# run simulate_business_service.py
print("Running simulate_business_service.py")
subprocess.run(["python", "simulate_business_service.py"], check=True)

# run simulate_customer.py
print("Running simulate_customer.py")
subprocess.run(["python", "simulate_customer.py"], check=True)

# run simulate_appointment.py
print("Running simulate_appointment.py")
subprocess.run(["python", "simulate_appointment.py"], check=True)

# run simulate_staff_work_timesheet.py
print("Running simulate_staff_work_timesheet.py")
subprocess.run(["python", "simulate_staff_work_timesheet.py"], check=True)

# run simulate_loyalty_card.py
print("Running simulate_loyalty_card.py")
subprocess.run(["python", "simulate_loyalty_card.py"], check=True)


print("All simulations have been run successfully!")
