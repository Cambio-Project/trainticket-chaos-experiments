import requests

# Log into the TrainTicket system
login_response = requests.post(f"http://localhost:8080/api/v1/users/login", json = {"username": "admin", "password": "222222"})
login_response_parsed = login_response.json()
auth_header = {'Authorization': f"Bearer {login_response_parsed['data']['token']}"}
user_id = login_response_parsed['data']['userId']
# print(login_response_parsed)

# Reserve a ticket, we do however not get the order ID back from the reservation ("preserve") service
trip_id = "D1345"
reserve_json = {
    "accountId":"4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
    "contactsId":"eaaa553d-919b-4260-8592-a05ec7bbf120",
    "tripId":trip_id,
    "seatType":"2",
    "date":"2021-04-15",
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

payment_result = requests.post("http://localhost:18673/api/v1/inside_pay_service/inside_payment", json=payment_json, headers=auth_header)
print(f"INFO: Order ID is {order_id}")

# Query payments/orders and check whether payment has actually worked
payment_query_result = requests.get("http://localhost:18673/api/v1/inside_pay_service/inside_payment/payment", headers=auth_header)
print(payment_query_result.json())