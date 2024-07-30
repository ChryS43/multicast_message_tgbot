from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, User
import asyncio

API_ID = ""
API_HASH = ""
LIMIT = 100  # Limit of chats to retrieve per batch
MESSAGE_DELAY = 5  # Delay in seconds between each message

message = """
⭐️✨⭐️✨⭐️✨⭐️✨⭐️✨⭐️✨

👋 <b>CIAO!</b> Questo è un messaggio automatico per tutti i nostri clienti. Volevamo informarti della <b>PROMO FINE CAMPIONATO</b>! Come ogni anno, questa promo è valida per tutti, sia per chi deve rinnovare, sia per chi già possiede una linea attiva.

📌 <b>Dettagli dell'offerta:</b>
- 6 mesi: <b>45€</b> 🔥
- 12 mesi: <b>80€</b> 🔥🔥

🥳 <b>Non perderti questa occasione!</b>

➡️ Per aderire all'offerta, contattaci subito:
@teamfrancobollotv
@teamfrancobollotv
@teamfrancobollotv

⚠️ <b>Nota:</b> Se non sei un cliente o non vuoi aderire all'offerta, ignora questo messaggio. Grazie! 🙏

✨⭐️✨⭐️✨⭐️✨⭐️✨⭐️✨
"""

def get_input(prompt):
    return input(prompt).strip()

async def get_phone_and_message():
    phone = get_input('Enter your phone number (including international code, e.g., +391234567890): ')
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
                    await client.send_message(entity.id, message, parse_mode='html')
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

    phone = await get_phone_and_message()
    await client.start(phone)

    print("Successfully logged in!")

    await send_messages(client, message)

if __name__ == '__main__':
    asyncio.run(main())
