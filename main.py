from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, User
import asyncio

API_ID = "8339070"
API_HASH = "f65352465cb4bc25779336627a19112d"
LIMIT = 100  # Limit of chats to retrieve per batch
MESSAGE_DELAY = 5  # Delay in seconds between each message

def get_input(prompt):
    return input(prompt).strip()

async def get_phone_and_message():
    phone = get_input('Enter your phone number (including international code, e.g., +391234567890): ')
    message = get_input('Enter the message to send to all contacts: ')
    return phone, message

async def send_messages(client, message):
    offset_id = 0

    while True:
        # Get the list of recent chats
        dialogs = await client(GetDialogsRequest(
            offset_date=None,
            offset_id=offset_id,
            offset_peer=InputPeerEmpty(),
            hash=0,
            limit=LIMIT
        ))

        if not dialogs.dialogs:
            print("No more dialogs to process.")
            break

        for dialog in dialogs.dialogs:
            try:
                # Get the peer entity
                entity = await client.get_entity(dialog.peer)
                if isinstance(entity, User):
                    if entity.bot:
                        # Skip bots
                        continue
                    print(f"Sending message to {entity.first_name} {entity.last_name or ''}...")
                    await client.send_message(entity.id, message)
                    print(f"Message sent to {entity.first_name} {entity.last_name or ''}.")
                    await asyncio.sleep(MESSAGE_DELAY)
            except Exception as e:
                print(f"Error sending message to {entity.first_name} {entity.last_name or ''}: {e}")

        # Update offset_id to the last dialog's ID
        if dialogs.dialogs:
            offset_id = dialogs.dialogs[-1].id  # Use the ID of the last dialog

        # Ask user if they want to continue
        continue_choice = get_input('Do you want to continue with the next batch of chats? (yes/no): ').lower()
        if continue_choice != 'yes':
            break

async def main():
    client = TelegramClient('anon', API_ID, API_HASH)

    phone, message = await get_phone_and_message()
    await client.start(phone)

    print("Successfully logged in!")

    await send_messages(client, message)

if __name__ == '__main__':
    asyncio.run(main())
