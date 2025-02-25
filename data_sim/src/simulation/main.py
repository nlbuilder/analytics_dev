import subprocess
import os, sys

# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)


# run simulate_business.py
print("Running simulate_business.py")
subprocess.run(["python", os.path.join(script_path, "simulate_business.py")], check=True)

# run simulate_business_service.py
print("Running simulate_business_service.py")
subprocess.run(["python", os.path.join(script_path, "simulate_business_service.py")], check=True)

# run simulate_customer.py
print("Running simulate_customer.py")
subprocess.run(["python", os.path.join(script_path, "simulate_customer.py")], check=True)

# run simulate_appointment.py
print("Running simulate_appointment.py")
subprocess.run(["python", os.path.join(script_path, "simulate_appointment.py")], check=True)

# run simulate_staff_work_timesheet.py
print("Running simulate_staff_work_timesheet.py")
subprocess.run(["python", os.path.join(script_path, "simulate_staff_work_timesheet.py")], check=True)

# run simulate_loyalty_card.py
print("Running simulate_loyalty_card.py")
subprocess.run(["python", os.path.join(script_path, "simulate_loyalty_card.py")], check=True)


print("All simulations have been run successfully!")
