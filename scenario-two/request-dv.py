import requests
import datetime

# Log into the TrainTicket system
login_response = requests.post(f"http://localhost:8080/api/v1/users/login", json = {"username": "admin", "password": "222222"})
login_response_parsed = login_response.json()
auth_header = {'Authorization': f"Bearer {login_response_parsed['data']['token']}"}
user_id = login_response_parsed['data']['userId']
# print(login_response_parsed)

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
print(f"Reservation JSON object: {reserve_json}")
reserve_response = requests.post("http://localhost:14568/api/v1/preserveservice/preserve", json=reserve_json, headers=auth_header)
print(f"Reservation response: {reserve_response.json()}")

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
order_ids = [payment["orderId"] for payment in payment_query_result.json()["data"]]
print(order_ids)