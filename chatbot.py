
!pip install pandas numpy transformers mysql-connector-python flask
import pandas as pd
import numpy as np
from transformers import pipeline
import mysql.connector
from google.colab import drive


drive.mount('/content/drive')


data = pd.read_csv('/content/drive/MyDrive/telematics_data.csv')

data.dropna(inplace=True)

intent_recognizer = pipeline("zero-shot-classification")


def get_intent(user_query):
    labels = ["battery status", "distance traveled", "fault check"]
    result = intent_recognizer(user_query, candidate_labels=labels)
    return result['labels'][0]
# Establish database connection
connection = mysql.connector.connect(
    host="your-database-host",
    user="username",
    password="password",
    database="telematics_db"
)


def get_battery_status(vehicle_id):
    cursor = connection.cursor()
    cursor.execute(f"SELECT battery_health FROM battery_stats WHERE vehicle_id = '{vehicle_id}'")
    result = cursor.fetchone()
    return result[0] if result else "Battery status not found."


def get_distance_traveled(vehicle_id):
    cursor = connection.cursor()
    cursor.execute(f"SELECT distance_traveled FROM ride_stats WHERE vehicle_id = '{vehicle_id}'")
    result = cursor.fetchone()
    return result[0] if result else "Distance data not found."


def check_vehicle_fault(vehicle_id):
    cursor = connection.cursor()
    cursor.execute(f"SELECT fault_code FROM faults WHERE vehicle_id = '{vehicle_id}'")
    result = cursor.fetchall()
    return [fault[0] for fault in result] if result else ["No faults found."]
def chatbot_response(user_query, vehicle_id="1234"):
    
    intent = get_intent(user_query)

    
    if intent == "battery status":
        response = get_battery_status(vehicle_id)
        return f"Battery Health: {response}"
    elif intent == "distance traveled":
        response = get_distance_traveled(vehicle_id)
        return f"Distance Traveled: {response} km"
    elif intent == "fault check":
        faults = check_vehicle_fault(vehicle_id)
        return f"Current Faults: {', '.join(faults)}"
    else:
        return "I'm sorry, I didn't understand that. Could you rephrase?"


print(chatbot_response("What is the current battery status?", vehicle_id="1234"))
print(chatbot_response("How far did the vehicle travel today?", vehicle_id="1234"))
print(chatbot_response("Is there any fault with the vehicle right now?", vehicle_id="1234"))
while True:
    user_input = input("Ask something about your vehicle's status (type 'exit' to stop): ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    response = chatbot_response(user_input)
    print(response)
