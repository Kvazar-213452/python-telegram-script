from telethon import TelegramClient, events
from datetime import datetime
import asyncio
from func import (
    check_auto_meessage,
    auto_del_meessage,
    text_log_write,
    get_location,
    load_accounts,
    block_users,
    unlocked_users,
    scams_message
)

message_store = {}

async def handle_account(api_id, api_hash, phone_number):
    client = TelegramClient(f'session_{phone_number}', api_id, api_hash)

    @client.on(events.NewMessage())
    async def handler(event):
        message = event.message.message
        chat_id = event.chat_id
        message_id = event.message.id
        sender_id = event.sender_id

        scams_message(sender_id, message)
        message_store[(chat_id, message_id)] = message

        let_1 = check_auto_meessage(message)
        if let_1:
            await client.send_message(chat_id, let_1)

        let_2 = auto_del_meessage(message)
        if let_2:
            await client.delete_messages(chat_id, message_id)

        if event.is_private:
            text_log_write(message, "message_private", chat_id)

        elif event.is_group:
            text_log_write(message, "message_group", chat_id)

        elif event.is_channel:
            text_log_write(message, "message_chenel", chat_id)

    @client.on(events.NewMessage(incoming=True))
    async def incoming_message_handler(event):
        message = event.message.message
        chat_id = event.chat_id

        if event.is_private:
            text_log_write(message, "someone_message_private", chat_id)

        elif event.is_group:
            text_log_write(message, "someone_message_group", chat_id)

        elif event.is_channel:
            text_log_write(message, "someone_message_chennel", chat_id)

    @client.on(events.MessageEdited())
    async def handle_message_edited(event):
        message = event.message.message
        chat_id = event.chat_id

        if event.is_private:
            text_log_write(message, "edited_message_private", chat_id)

        elif event.is_group:
            text_log_write(message, "edited_message_group", chat_id)

        elif event.is_channel:
            text_log_write(message, "edited_message_chenel", chat_id)

    @client.on(events.MessageDeleted())
    async def handle_message_deleted(event):
        chat_id = event.chat_id

        for message_id in event.deleted_ids:
            message = message_store.get((chat_id, message_id))
            if message:
                text_log_write(message + " del " + str(message_id), "del_message", chat_id)
                del message_store[(chat_id, message_id)]

    # Log location and start time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    city, country, loc = get_location()

    log_filename = f"start_{phone_number}.log"
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(f"Current time: {current_time}\n")
        if city and country:
            log_file.write(f"Location: {city}, {country} (Coordinates: {loc})\n\n")
        else:
            log_file.write(f"Failed to get location.\n\n")

    await client.start(phone_number)
    print(f"Account {phone_number} is now running...")

    await block_users(client)  
    await unlocked_users(client) 

    await client.run_until_disconnected()

async def main():
    accounts = load_accounts('conf/start.json')
    tasks = []

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    city, country, loc = get_location()

    with open(f"log_app/start.log", "a", encoding="utf-8") as file:
        file.write(f"Current time: {current_time}\n")
        if city and country:
            file.write(f"Location: {city}, {country} (Coordinates: {loc})\n\n")
        else:
            file.write(f"Failed to get location.\n\n")

    for api_id, api_hash, phone_number in accounts:
        task = asyncio.create_task(handle_account(api_id, api_hash, phone_number))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())