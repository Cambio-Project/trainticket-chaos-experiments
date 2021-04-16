#!/usr/bin/python3
import os
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

def scenario_two_steady_state_probe():
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
        return False

    return True