import asyncio
import csv
import os
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerUser
from argparse import ArgumentParser
import re


# Parsing command line arguments
parser = ArgumentParser(description="Invia messaggi Telegram.")
parser.add_argument("phone", help="Numero di telefono (con prefisso internazionale, es. +393473369041).")
parser.add_argument("message_file", help="Percorso del file di testo contenente il messaggio.")
parser.add_argument("csv_file", help="Nome del file CSV per tenere traccia degli utenti a cui è stato inviato il messaggio.")
parser.add_argument("delay", type=int, help="Tempo di attesa in secondi tra l'invio di ogni messaggio.")
parser.add_argument("session", type=str, help="Nome della sessione di Telethon")
args = parser.parse_args()

# Telegram API credentials
api_id = '22898767'
api_hash = 'a207ea63fb8ae1eafa3680f54c989b7d'
client = TelegramClient('test_session', api_id, api_hash)

# Verifica se i file esistono
if not os.path.exists(args.message_file):
    print(f"Errore: Il file di messaggio '{args.message_file}' non esiste.")
    exit(1)

def normalize_message(text):
    """Normalizza il messaggio rimuovendo spazi extra, uniformando le maiuscole/minuscole e rimuovendo i tag HTML."""
    text = re.sub(r'<.*?>', '', text)  # Rimuove i tag HTML
    return text

async def is_message_already_sent(user, message):
    """Check if the message has already been sent in the last 10 messages with the user."""
    messages = await client.get_messages(user, limit=10)
    normalized_message = normalize_message(message)
    for msg in messages:
        if msg.message == normalized_message:
            return True
    return False

# Read message from file
with open(args.message_file, 'r', encoding='utf-8') as file:
    message = file.read()

async def main():
    await client.start(args.phone)

    # Load already messaged users from CSV
    sent_users = set()
    if os.path.exists(args.csv_file):
        with open(args.csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            sent_users = {int(row[0]) for row in reader}

    last_date = None
    chunk_size = 200
    has_more = True

    while has_more:
        result = await client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))

        if not result.dialogs:
            has_more = False
            break

        with open(args.csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            for dialog in result.dialogs:
                if isinstance(dialog.peer, PeerUser):
                    user = await client.get_entity(dialog.peer.user_id)

                    if user.id not in sent_users:
                        try:
                            if await is_message_already_sent(user, message):
                                print(f"Il messaggio è già stato inviato a {user.first_name} {user.last_name} - ID: {user.id}")
                                continue
                            # Uncomment the line below to send the message
                            if user.first_name == "ChryS":
                                await client.send_message(user.id, message, parse_mode='html')
                            print(f"Messaggio inviato a: {user.first_name} {user.last_name} - ID: {user.id}")
                            writer.writerow([user.id, user.first_name, user.last_name])
                            sent_users.add(user.id)
                            await asyncio.sleep(args.delay)
                        except Exception as e:
                            print(f"Errore nell'invio del messaggio a {user.first_name} {user.last_name}: {e}")

        if result.messages:
            last_date = min(msg.date for msg in result.messages)

with client:
    client.loop.run_until_complete(main())
