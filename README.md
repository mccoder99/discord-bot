# mccoder99 | Open Source Files
## 🤖 Discord Bot
Hier habe ich für euch einen Discord Bot in Python der mithilfe von Ezcord und Pycord erstellt wurde,
welcher sehr viele umfangreiche Funktionen besitzt. Der Bot unterstützt die deutsche Sprache!
## 📦 Packages
- PyNaCl
- easy_pil
- asyncpraw
- requests
- aiosqlite
- ezcord
- python-dotenv
## 📋 Features
Der Bot hat allgemeine Befehle wie Info Commands, Fun-Befehle wie einen Meme Command, ein umfangreiches
Moderationssystem mit Timeout Command, ein Levelsystem mit Rangkarte, einen Ticket-Support mit integriertem
Logging-System, Radio Befehle für 24/7 Musik und einen Global-Chat. Er hat außerdem die neuesten Funktionen der Discord
API - z.B.: Slash Commands, Dropdowns und Buttons.
## 🛠️ Einrichtung
Bevor du den Bot ausführen kannst, musst du einige Konfigurationen festlegen. Erstelle eine `.env`-Datei im
Hauptverzeichnis des Projekts. Ersetze `<BOT_TOKEN>` durch deinen tatsächlichen Bot-Token,
den du von der Discord-Entwicklerwebseite erhalten hast. Den `API_KEY` erhälst du auf der
[Google Developers](https://developers.google.com/tenor/guides/quickstart) Webseite,
für unsere Zwecke wird ein Key der Tenor API benötigt.
Für die `CLIENT_ID` und das `CLIENT_SECRET` kannst du die Daten einsetzen,
welche du auf [Reddit](https://www.reddit.com/prefs/apps/) erhälst. Ersetze `<PASSWORD>` durch dein Passwort von Reddit.
Die Variable `<ERROR_WEBHOOK_URL>` kannst du durch eine Webhook-URL ersetzen,
in diesen Kanal werden Error Reports gesendet.
```
BOT_TOKEN = <BOT_TOKEN>
API_KEY = <API_KEY>
CLIENT_ID = <CLIENT_ID>
CLIENT_SECRET = <CLIENT_SECRET>
PASSWORD = <PASSWORD>
ERROR_WEBHOOK_URL = <ERROR_WEBHOOK_URL>
```
Um den Bot auszuführen, müssen zuerst alle erforderlichen Pakete installiert werden.  
Das machst du mit dem folgenden Befehl:
```
pip install -r requirements.txt
```
