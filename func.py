from datetime import datetime
from telethon import functions
import json
import requests


with open('conf/data.json', 'r') as file:
    config = json.load(file)

def text_log_write(message, file, chat_id):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(f"data/{file}.log", "a", encoding="utf-8") as file:
        file.write(f"{chat_id} || {message} - {current_time}\n")

def check_auto_meessage(message):
    mas = config['auto_meessage']
    i = 0 
    while i < len(mas):
        if message == mas[i][0]:
            return mas[i][1]
        i += 1
    return False

def get_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        return data['city'], data['country'], data['loc']
    except Exception as e:
        print(f"Failed to get location: {e}")
        return None, None, None
    
def auto_del_meessage(message):
    mas = config['auto_del_meessage']
    i = 0 
    while i < len(mas):
        if message == mas[i]:
            return mas[i]
        i += 1
    return False

def load_accounts(file):
    with open(file, 'r') as f:
        return json.load(f)
    
def log_write_app_b_u_locked(phone_number):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(f"log_app/b_u_users.log", "a", encoding="utf-8") as file:
        file.write(f"User with number {phone_number} - {current_time}\n")

async def block_user_by_phone(client, phone_number):
    try:
        user = await client.get_entity(phone_number)
        await client(functions.contacts.BlockRequest(user.id))
        log_write_app_b_u_locked(phone_number + " blocked")
    except Exception as e:
        print(f"Error: {e}")

async def unblock_user_by_phone(client, phone_number):
    await client.start()

    try:
        user = await client.get_entity(phone_number)
        
        await client(functions.contacts.UnblockRequest(user.id))
        log_write_app_b_u_locked(phone_number + " unlocked")
    except Exception as e:
        print(f"Error: {e}")

async def block_users(client):
    with open('conf/block_users.json', 'r') as file:
        config = json.load(file)

    for phone_number in config:
        await block_user_by_phone(client, phone_number)

async def unlocked_users(client):
    with open('conf/unlocked_users.json', 'r') as file:
        config = json.load(file)

    for phone_number in config:
        await unblock_user_by_phone(client, phone_number)

def scams_message(sender_id, message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('conf/scams.json', 'r') as file:
        config = json.load(file)
    i = 0
    while i < len(config):
        if config[i] == sender_id:
            with open(f"data/scams.log", "a", encoding="utf-8") as file:
                file.write(f"A message has been written {sender_id} || {message} - {current_time}\n")
        i += 1