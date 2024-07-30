import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerUser

phone = input("Inserisci il numero di telefono (con il prefisso internazionale, es. +393473369041): ")

api_id = '22898767'
api_hash = 'a207ea63fb8ae1eafa3680f54c989b7d'

client = TelegramClient('test_session', api_id, api_hash)

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

async def main():
    await client.start(phone)

    last_date = None
    chunk_size = 200
    has_more = True
    sended_message = 0

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

        for dialog in result.dialogs:
            if isinstance(dialog.peer, PeerUser):
                user = await client.get_entity(dialog.peer.user_id)

                try:
                    # await client.send_message(user.id, message, parse_mode='html')
                    print(f"Messaggio inviato a: {user.first_name} {user.last_name} - ID: {user.id}")
                    sended_message += 1
                    print(f"Numero di messaggi inviati: {sended_message}")
                    await asyncio.sleep(2)
                except Exception as e:
                    print(f"Errore nell'invio del messaggio a {user.first_name} {user.last_name}: {e}")

        if result.messages:
            last_date = min(msg.date for msg in result.messages)
    

with client:
    client.loop.run_until_complete(main())
