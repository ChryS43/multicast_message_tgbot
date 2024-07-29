# Telegram Userbot

Questo progetto è uno script userbot per Telegram che permette di inviare messaggi a contatti specifici.

## Prerequisiti

- Python 3.7 o superiore
- Git

## Installazione

1. Clona il repository:
git clone https://github.com/tuoUsername/telegram-userbot.git
cd telegram-userbot
Copy
2. Crea un ambiente virtuale:
python -m venv venv
Copy
3. Attiva l'ambiente virtuale:
- Su Windows:
  ```
  venv\Scripts\activate
  ```
- Su macOS e Linux:
  ```
  source venv/bin/activate
  ```

4. Installa le dipendenze:
pip install -r requirements.txt
Copy
## Configurazione

1. Apri il file `userbot.py` con un editor di testo.

2. Sostituisci i valori vuoti di `API_ID` e `API_HASH` con le tue credenziali Telegram:
```python
API_ID = "il_tuo_api_id"
API_HASH = "il_tuo_api_hash"
Per ottenere queste credenziali:

Vai su https://my.telegram.org
Accedi con il tuo numero di telefono
Clicca su "API development tools"
Crea una nuova applicazione

Utilizzo

Esegui lo script:
Copypython main.py

Inserisci il tuo numero di telefono quando richiesto (incluso il prefisso internazionale, es. +391234567890).
Inserisci il messaggio che vuoi inviare.
Lo script inizierà a processare i tuoi contatti. Invierà il messaggio solo ai contatti il cui nome è "ChryS".
Dopo ogni batch di contatti, ti verrà chiesto se vuoi continuare con il prossimo batch. Rispondi 'yes' per continuare o qualsiasi altra cosa per fermarti.

Note

Lo script invierà messaggi solo ai contatti il cui nome è esattamente "ChryS".
C'è un ritardo di 5 secondi tra ogni messaggio inviato per evitare di superare i limiti di invio di Telegram.
Assicurati di utilizzare questo script in modo responsabile e in conformità con i termini di servizio di Telegram.


