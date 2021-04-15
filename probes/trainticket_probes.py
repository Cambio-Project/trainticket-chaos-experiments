#!/usr/bin/python3
import os

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
    # Game plan:
    # (1) Make a valid reservation that should then show up in the TT order list
    # (2) Pay for that order
    # (3) Query the inside_payment service to see whether payment was successful

    return True