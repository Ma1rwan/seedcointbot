# bot/create_session.py
import os
import json
from pyrogram import Client

def create_session():
    with open("config.json", "r") as json_file:
        data = json.load(json_file)
    api_id = data.get("API_ID")
    api_hash = data.get("API_HASH")

    # Ask user to input the session name
    session_name = input("Enter session name: ")

    # Create the /sessions folder if it doesn't exist
    session_folder = "sessions"
    os.makedirs(session_folder, exist_ok=True)

    # Define the session file path
    session_path = os.path.join(session_folder, session_name)

    # Create a client session
    with Client(session_path, api_id, api_hash) as app:
        print(f"{session_name} Session created successfully!")

