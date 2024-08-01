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
parser.add_argument("pause_after", type=int, help="Numero di richieste dopo le quali prendersi una pausa.")
parser.add_argument("pause_duration", type=int, help="Durata della pausa in secondi.")
args = parser.parse_args()

# Telegram API credentials
api_id = '22898767'
api_hash = 'a207ea63fb8ae1eafa3680f54c989b7d'
client = TelegramClient(args.session, api_id, api_hash)

# Verifica se i file esistono
if not os.path.exists(args.message_file):
    print(f"Errore: Il file di messaggio '{args.message_file}' non esiste.")
    exit(1)

def normalize_message(text):
    """Normalizza il messaggio rimuovendo spazi extra, uniformando le maiuscole/minuscole e rimuovendo i tag HTML."""
    return re.sub(r'<.*?>', '', text)  # Rimuove i tag HTML

async def is_message_already_sent(user, message):
    """Controlla se il messaggio è già stato inviato tra gli ultimi 20 messaggi con l'utente."""
    messages = await client.get_messages(user, limit=20)
    normalized_message = normalize_message(message)
    for msg in messages:
        if msg.message == normalized_message:
            return True
    return False

# Legge il messaggio dal file
with open(args.message_file, 'r', encoding='utf-8') as file:
    message = file.read()

async def main():
    await client.start(args.phone)

    # Carica gli utenti già contattati dal file CSV
    sent_users = set()
    if os.path.exists(args.csv_file):
        with open(args.csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            sent_users = {int(row[0]) for row in reader}

    last_date = None
    chunk_size = 200
    has_more = True
    requests_count = 0

    while has_more:
        result = await client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))

        requests_count += 1  # Incremento per la richiesta dei dialoghi

        if not result.dialogs:
            has_more = False
            break

        with open(args.csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            for dialog in result.dialogs:
                if isinstance(dialog.peer, PeerUser):
                    user = await client.get_entity(dialog.peer.user_id)
                    requests_count += 1  # Incremento per la richiesta dell'entità utente

                    if user.id not in sent_users:
                        try:
                            if await is_message_already_sent(user, message):
                                requests_count += 1
                                print(f"Il messaggio è già stato inviato a {user.first_name} {user.last_name} - ID: {user.id}")
                                continue
                            await client.send_message(user.id, message, parse_mode='html')
                            print(f"Messaggio inviato a: {user.first_name} {user.last_name} - ID: {user.id}")
                            writer.writerow([user.id, user.first_name, user.last_name])
                            sent_users.add(user.id)
                            requests_count += 1  # Incremento per la richiesta di invio messaggio
                            await asyncio.sleep(args.delay)

                            # Check if we need to take a pause
                            if requests_count >= args.pause_after:
                                print(f"Prendendo una pausa di {args.pause_duration} secondi dopo {requests_count} richieste.")
                                await asyncio.sleep(args.pause_duration)
                                requests_count = 0
                        except Exception as e:
                            print(f"Errore nell'invio del messaggio a {user.first_name} {user.last_name}: {e}")
                            print(f"Prendendo una pausa di {args.pause_duration} secondi")
                            await asyncio.sleep(args.pause_duration)

        if result.messages:
            last_date = min(msg.date for msg in result.messages)

with client:
    client.loop.run_until_complete(main())
