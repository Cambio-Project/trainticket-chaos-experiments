#!/usr/bin/python3
import os
import subprocess
import time
import random
import yaml

import requests
import datetime

import pandas as pd


# If you know your ticket booking system like you know yourself,
# you need not fear the result of a hundred train trips.
# -- Sun Tzu, probably

def steady_state_load():
    os.system(f"{os.getcwd()}/steady-state.sh")
    print("Execution of shell script finished. Evaluating responses.")
    csv_df = pd.read_csv("steady-log.csv")
    csv_df["Avg Response Time"].replace(0, float('nan')) # Remove zeroes, as they make the average meaningless
    mean_avg_response_time = csv_df["Avg Response Time"].mean()

    print(f"Average response time is: {mean_avg_response_time}")
    response_time_ok = mean_avg_response_time < 0.5
    return bool(response_time_ok) # Workaround to really stupid numpy behaviour (FIXME)


def food_service_overload_action():
    os.system(f"{os.getcwd()}/overload.sh")
    print("Finished overloading the food service, CSV is ready.")


def food_service_overload_probe():
    csv_df = pd.read_csv("overload-log.csv")
    csv_df["Avg Response Time"].replace(0, float('nan'))
    mean_avg_response_time = csv_df["Avg Response Time"].mean()

    print(f"Average time during overload is: {mean_avg_response_time}")
    response_time_ok = mean_avg_response_time < 0.5 # Workaround due to numpy being dumb, same as above: FIXME
    return bool(response_time_ok)


# Kills all loadgenerator processes
def kill_load_generators():
    os.system("pkill -f loadgenerator")


def scenario_two_steady_state_probe():
    # Start the Load Generator to create background load reflecting user interaction with the system
    os.system(f"{os.getcwd()}/steady-state.sh")
    print("Loadgenerators started, beginning steady state check")

    # Log in to TrainTicket to be authorized for subsequent requests
    login_response = requests.post(f"http://localhost:8080/api/v1/users/login", json = {"username": "admin", "password": "222222"})
    login_response_parsed = login_response.json()
    auth_header = {'Authorization': f"Bearer {login_response_parsed['data']['token']}"}
    user_id = login_response_parsed['data']['userId']

    # Get a contact id, we need that for reservations
    contacts_response = requests.get("http://localhost:12347/api/v1/contactservice/contacts", headers=auth_header)
    contact = contacts_response.json()["data"][0]
    contact_id = contact["id"]
    account_id = contact["accountId"]

    # Reserve a ticket, we do however not get the order ID back from the reservation ("preserve") service
    trip_id = "D1345"
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    reserve_json = {
        "accountId": account_id,
        "contactsId": contact_id,
        "tripId":trip_id,
        "seatType":"2",
        "date": tomorrow.strftime("%Y-%m-%d"),
        "from":"Shang Hai",
        "to":"Su Zhou",
        "assurance":"0",
        "foodType":1,
        "foodName":"Bone Soup",
        "foodPrice":2.5,
        "stationName":"",
        "storeName":""
    }
    reserve_response = requests.post("http://localhost:14568/api/v1/preserveservice/preserve", json=reserve_json, headers=auth_header)
    #print(f"Reservation response: {reserve_response.json()}")
    if not reserve_response.json()["status"] == 1:
        print("Reservation failed, failing this probe.")
        kill_load_generators()
        return False

    # Fetch the newest order, which _should_ be the one we just created
    all_orders = requests.get("http://localhost:12031/api/v1/orderservice/order", headers=auth_header)
    all_orders_list = all_orders.json()["data"]
    newest_order = sorted(all_orders_list, key=lambda order: order["boughtDate"], reverse=True)[0]

    # Pay for the order using inside_payment service
    price = "50.0"
    order_id = newest_order["id"]
    payment_json = {
        "orderId": order_id,
        "price": price,
        "tripId": trip_id,
        "userId": user_id
    }

    requests.post("http://localhost:18673/api/v1/inside_pay_service/inside_payment", json=payment_json, headers=auth_header)
    #print(f"INFO: Order ID is {order_id}")

    # Query payments/orders and check whether payment has actually worked (meaning that a payment entity exists for the order)
    payment_query_result = requests.get("http://localhost:18673/api/v1/inside_pay_service/inside_payment/payment", headers=auth_header)
    paid_order_ids = [payment["orderId"] for payment in payment_query_result.json()["data"]]
    if order_id not in paid_order_ids:
        print("No payment exists for this order - failing the probe.")
        kill_load_generators()
        return False

    print("Everything successful, ending experiment with success.")
    kill_load_generators()
    return True


def scenario_two_switch_bad_config():
    print("Switching database configs to bad one")
    os.system(f"{os.getcwd()}/switch-mongo-configs.sh")


def scenario_two_rollback_config():
    print("Switching back to good config")
    os.system(f"{os.getcwd()}/rollback-mongo-config.sh")


def scenario_two_broken_probe():
    # Start the Load Generator to create background load reflecting user interaction with the system
    os.system(f"{os.getcwd()}/steady-state.sh")
    print("Loadgenerators started, beginning steady state check")

    # Log in to TrainTicket to be authorized for subsequent requests
    login_response = requests.post(f"http://localhost:8080/api/v1/users/login", json = {"username": "admin", "password": "222222"})
    login_response_parsed = login_response.json()
    auth_header = {'Authorization': f"Bearer {login_response_parsed['data']['token']}"}
    user_id = login_response_parsed['data']['userId']

    # Get a contact id, we need that for reservations
    contacts_response = requests.get("http://localhost:12347/api/v1/contactservice/contacts", headers=auth_header)
    contact = contacts_response.json()["data"][0]
    contact_id = contact["id"]
    account_id = contact["accountId"]

    # Reserve a ticket, we do however not get the order ID back from the reservation ("preserve") service
    trip_id = "D1345"
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    reserve_json = {
        "accountId": account_id,
        "contactsId": contact_id,
        "tripId":trip_id,
        "seatType":"2",
        "date": tomorrow.strftime("%Y-%m-%d"),
        "from":"Shang Hai",
        "to":"Su Zhou",
        "assurance":"0",
        "foodType":1,
        "foodName":"Bone Soup",
        "foodPrice":2.5,
        "stationName":"",
        "storeName":""
    }
    reserve_response = requests.post("http://localhost:14568/api/v1/preserveservice/preserve", json=reserve_json, headers=auth_header)
    #print(f"Reservation response: {reserve_response.json()}")
    if not reserve_response.json()["status"] == 1:
        print("Reservation failed, failing this probe.")
        kill_load_generators()
        return False

    # Fetch the newest order, which _should_ be the one we just created
    all_orders = requests.get("http://localhost:12031/api/v1/orderservice/order", headers=auth_header)
    all_orders_list = all_orders.json()["data"]
    newest_order = sorted(all_orders_list, key=lambda order: order["boughtDate"], reverse=True)[0]

    # Pay for the order using inside_payment service
    price = "50.0"
    order_id = newest_order["id"]
    payment_json = {
        "orderId": order_id,
        "price": price,
        "tripId": trip_id,
        "userId": user_id
    }

    requests.post("http://localhost:18673/api/v1/inside_pay_service/inside_payment", json=payment_json, headers=auth_header)
    #print(f"INFO: Order ID is {order_id}")

    # Query payments/orders and check whether payment has actually worked (meaning that a payment entity exists for the order)
    payment_query_result = requests.get("http://localhost:18673/api/v1/inside_pay_service/inside_payment/payment", headers=auth_header)
    paid_order_ids = [payment["orderId"] for payment in payment_query_result.json()["data"]]
    if order_id not in paid_order_ids:
        print("No payment exists for this order - fault is happening.")
        kill_load_generators()
        return True

    print("The order has been paid, indicating that the fault injection failed.")
    kill_load_generators()
    return False
    

def scenario_three_steady_state_probe():
    # TODO: Move this login/auth part into a new function to avoid duplicate code
    # Start the Load Generator to create background load reflecting user interaction with the system
    os.system(f"{os.getcwd()}/steady-state.sh")
    print("Loadgenerators started, beginning steady state check")

    # Log in to TrainTicket to be authorized for subsequent requests
    login_response = requests.post(f"http://localhost:8080/api/v1/users/login", json = {"username": "admin", "password": "222222"})
    login_response_parsed = login_response.json()
    auth_header = {'Authorization': f"Bearer {login_response_parsed['data']['token']}"}
    user_id = login_response_parsed['data']['userId']

    # Get a contact id, we need that for reservations
    contacts_response = requests.get("http://localhost:12347/api/v1/contactservice/contacts", headers=auth_header)
    contact = contacts_response.json()["data"][0]
    contact_id = contact["id"]
    account_id = contact["accountId"]

    # TODO: Move ticket reservation part into a new function to avoid duplicate code
    # Reserve a ticket, we do however not get the order ID back from the reservation ("preserve") service
    trip_id = "D1345"
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    reserve_json = {
        "accountId": account_id,
        "contactsId": contact_id,
        "tripId":trip_id,
        "seatType":"2",
        "date": tomorrow.strftime("%Y-%m-%d"),
        "from":"Shang Hai",
        "to":"Su Zhou",
        "assurance":"0",
        "foodType":1,
        "foodName":"Bone Soup",
        "foodPrice":2.5,
        "stationName":"",
        "storeName":""
    }
    reserve_response = requests.post("http://localhost:14568/api/v1/preserveservice/preserve", json=reserve_json, headers=auth_header)
    #print(f"Reservation response: {reserve_response.json()}")
    if not reserve_response.json()["status"] == 1:
        print("Reservation failed, failing this probe.")
        kill_load_generators()
        return False

    print("Everything successful, ending experiment with success.")
    kill_load_generators()
    return True


def scenario_three_switch_faulty_preserve_controller():
    print("Switching database configs to bad one")
    os.system(f"{os.getcwd()}/switch-preserve-controller.sh")


def scenario_three_rollback_preserve_controller():
    print("Switching back to good config")
    os.system(f"{os.getcwd()}/rollback-preserve-controller.sh")

def scenario_three_broken_probe():
    # Start the Load Generator to create background load reflecting user interaction with the system
    os.system(f"{os.getcwd()}/steady-state.sh")
    print("Loadgenerators started, beginning steady state check")

    # Log in to TrainTicket to be authorized for subsequent requests
    login_response = requests.post(f"http://localhost:8080/api/v1/users/login", json = {"username": "admin", "password": "222222"})
    login_response_parsed = login_response.json()
    auth_header = {'Authorization': f"Bearer {login_response_parsed['data']['token']}"}
    user_id = login_response_parsed['data']['userId']

    # Get a contact id, we need that for reservations
    contacts_response = requests.get("http://localhost:12347/api/v1/contactservice/contacts", headers=auth_header)
    contact = contacts_response.json()["data"][0]
    contact_id = contact["id"]
    account_id = contact["accountId"]

    # Reserve a ticket, we do however not get the order ID back from the reservation ("preserve") service
    trip_id = "D1345"
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    reserve_json = {
        "accountId": account_id,
        "contactsId": contact_id,
        "tripId":trip_id,
        "seatType":"2",
        "date": tomorrow.strftime("%Y-%m-%d"),
        "from":"Shang Hai",
        "to":"Su Zhou",
        "assurance":"0",
        "foodType":1,
        "foodName":"Bone Soup",
        "foodPrice":2.5,
        "stationName":"",
        "storeName":""
    }
    reserve_response = requests.post("http://localhost:14568/api/v1/preserveservice/preserve", json=reserve_json, headers=auth_header)
    #print(f"Reservation response: {reserve_response.json()}")
    if reserve_response.headers['Content-Type'] != "application/json":
        print("Response type is not JSON - fault is happening.")
        kill_load_generators()
        return True

    print("The response type is still JSON, indicating that the fault injection failed.")
    kill_load_generators()
    return False


# Returns after detecting that TrainTicket has bootet
def probe_wait_trainticket_running_k8s():
    trainticket_booted = False
    while not trainticket_booted:
        status = subprocess.getoutput("kubectl get pods | grep 0/1")
        trainticket_booted = not status
        print(f"Waiting 30 seconds. TrainTicket status is: {status}")
        time.sleep(30)
    return


# Waits until a pod error has occured
def probe_wait_poderror_trainticket_k8s():
    error_occured = False
    while not error_occured:
        pods = subprocess.getoutput("kubectl get pods | grep 0/1")
        number_of_lines = pods.count('\n')
        error_occured = ("Error" in pods or "CrashLoopBackOff" in pods) and number_of_lines < 10
        print(f"Waiting 15 seconds. Pod status is: {pods}")
        time.sleep(15)
    return


def twentyfive_percent_chance():
    nonce = random.randint(1, 4)
    return nonce == 1


def action_scramble_and_redeploy():
    invalid_dns_config = {'dnsPolicy': 'None', 'dnsConfig': {'nameservers': ['192.168.1.213']}}
    with open('quickstart-ts-deployment-part2.yml') as file:
        docs = yaml.load_all(file, Loader=yaml.FullLoader)
        scrambled_docs = []
        for doc in docs:
            if doc['kind'] == 'Deployment' and twentyfive_percent_chance():
                doc["spec"]["template"]["spec"].update(invalid_dns_config)

            scrambled_docs.append(doc)

        # This should overwrite the file in place, as according to: https://stackoverflow.com/a/53607914
        with open("scrambled-yaml.yaml", "w") as outfile:
            yaml.dump_all(scrambled_docs, outfile, default_flow_style=False)

    print("Finished scrambling, redeploying next.")
    os.system(f"{os.getcwd()}/replace-and-redeploy-2.sh")


def probe_all_pods_ok():
    pods = subprocess.getoutput("kubectl get pods")
    pod_rows = pods.splitlines()
    del pod_rows[0]
    faulty_pods_exist = False
    for row in pod_rows:
        faulty_pods_exist = not ("1/1" in row and "Running" in row)
        if faulty_pods_exist:
            break
    return not faulty_pods_exist