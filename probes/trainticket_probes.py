#!/usr/bin/python3
import os

import pandas as pd


# If you know your ticket booking system like you know yourself,
# you need not fear the result of a hundred train trips.
# -- Sun Tzu, probably

def hello_world(echo):
    print(f"Hello world from the TrainTicket hello world probe. Echo is: {echo}")
    return True


def steady_state_load():
    os.system(f"{os.getcwd()}/steady-state.sh")
    print("Execution of shell script finished. Evaluating responses")
    csv_df = pd.read_csv("steady-log.csv")
    csv_df["Avg Response Time"].replace(0, float('nan'))
    mean_avg_response_time = csv_df["Avg Response Time"].mean()

    print(f"Average response time is: {mean_avg_response_time}")
    response_time_ok = mean_avg_response_time < 0.5
    return bool(response_time_ok) # Workaround to really stupid numpy behaviour (TODO)


def overload_food_service(requests):
    # Plan for this function:
    # Spool up the load generator and launch a massive request spike that overloads the foodmap service
    # analyze the response times after the overload, maybe by returning the avg time again?
    return 66.6