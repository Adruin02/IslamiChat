[![Releases](https://img.shields.io/badge/Releases-Download-blue?logo=github&logoColor=white)](https://github.com/Adruin02/IslamiChat/releases)

# IslamiChat — Chatbot & Prayer Times Web App (Streamlit) ✨🕌

![Header image](https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1600&q=60)

IslamiChat combines an Islamic chatbot with prayer-time features. It runs on Streamlit. It supports Aladhan API for prayer times and can connect to IoT devices via MQTT. Use it for study, teaching, or home automation that respects prayer schedules.

Badges
- Topics: ai · aladhan-api · chatbot · education · iot · islam · prayer-times · python · streamlit · webapp
- Releases: [Download release assets](https://github.com/Adruin02/IslamiChat/releases)  
  Use the Releases page to get packaged builds or binaries. Download the release asset and run the provided start script or run the Python app.

Table of Contents
- Features
- Demo
- Tech stack
- Installation (local)
- Install from Releases
- Configuration
  - Aladhan API
  - MQTT / IoT
- Usage
  - Chat examples
  - Prayer notifications
- Deployment
  - Docker
  - Systemd service
- Contributing
- Files and structure
- License
- Contact

Features
- Chatbot with Islamic knowledge base. Supports Indonesian and English prompts.
- Prayer times using Aladhan API. Supports different calculation methods.
- Streamlit UI. Clean, mobile-friendly interface.
- MQTT integration for IoT. Publish prayer events to devices.
- Local caching for prayer times.
- Simple config via environment variables or config file.
- Extensible architecture for adding new models or data sources.

Demo screenshots
![App screenshot 1](https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d?auto=format&fit=crop&w=1200&q=60)
![App screenshot 2](https://images.unsplash.com/photo-1517816743773-6e0fd518b4a6?auto=format&fit=crop&w=1200&q=60)

Tech stack
- Python 3.10+
- Streamlit
- Requests (HTTP client)
- paho-mqtt (MQTT client)
- Optional: transformers or OpenAI client for AI model backends
- Aladhan API for prayer times
- Deployment: Docker, systemd

Quick local install (recommended)
1. Clone repo
   git clone https://github.com/Adruin02/IslamiChat.git
2. Create virtual environment
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows
3. Install dependencies
   pip install -r requirements.txt
4. Create config
   cp .env.example .env
   Edit .env to set your location and MQTT broker.
5. Run
   streamlit run app.py --server.port 8501

Install from Releases (download & execute)
The Releases page hosts packaged assets. Visit the Releases link and download the release file. The release asset contains a ready-to-run bundle and a start script.

- Visit: https://github.com/Adruin02/IslamiChat/releases
- Download asset (example name: IslamiChat-v1.0.zip)
- Unzip the archive
- Run the start script or run Streamlit directly
  - Unix
    ./start.sh
  - Windows
    .\start.bat
  - Or
    python -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

Configuration

Environment variables
Use .env or system env vars. Common vars:
- ALADHAN_METHOD: integer, calculation method (default 2)
- LATITUDE: float
- LONGITUDE: float
- TIMEZONE: UTC offset or tz database name
- MQTT_BROKER: host
- MQTT_PORT: port (default 1883)
- MQTT_TOPIC: topic to publish prayer events
- MODEL_BACKEND: "local" or "openai" or "other"

Aladhan API
IslamiChat uses Aladhan API for prayer times. The app calls the API with lat/lon or city. Set LATITUDE and LONGITUDE in .env or use the UI to let the app detect your location. The app caches the daily schedule in JSON to reduce API calls.

Sample request flow (internal)
- GET https://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method={method}
- Parse JSON, store prayer times in local_cache/{date}.json
- Compute next prayer and seconds until event

MQTT / IoT integration
IslamiChat can publish JSON events for IoT integration. Use paho-mqtt client.

Sample payload
{
  "event": "adhan_start",
  "prayer": "Fajr",
  "time": "05:10",
  "timestamp": 1680000000
}

Sample publish code (concept)
from paho.mqtt import client as mqtt_client

client = mqtt_client.Client("IslamiChat")
client.connect(MQTT_BROKER, MQTT_PORT)
payload = json.dumps({...})
client.publish(MQTT_TOPIC, payload)

Usage

Start the app
streamlit run app.py --server.port 8501

UI sections
- Chat: Ask questions about fiqh, dua, prayer meaning, or history.
- Prayer Times: View today’s times and monthly schedule.
- Settings: Set location, calculation method, and MQTT settings.
- Logs: View delivered MQTT events and API calls.

Chat examples
- "Apa arti niat shalat?"
- "How do I perform Wudu step by step?"
- "Give me morning duas in Arabic and their translation."
- "List conditions that break fasting."

Prayer notification examples
- When a prayer time begins, the app can:
  - Show an on-screen alert
  - Play an audio adhan file
  - Publish an MQTT message to notify a lamp, speaker, or home automation hub

Extended features to enable
- Use MODEL_BACKEND=openai to connect to OpenAI or other LLM. Set API key in env.
- Enable audio adhan: set ADHAN_AUDIO_URL or use local MP3.

Deployment

Docker
Dockerfile ships a minimal image. Build and run:
docker build -t islamichat:latest .
docker run -p 8501:8501 \
  -e LATITUDE=... -e LONGITUDE=... \
  -e MQTT_BROKER=... \
  islamichat:latest

Systemd service
Create /etc/systemd/system/islamichat.service
[Unit]
Description=IslamiChat Streamlit App
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/IslamiChat
EnvironmentFile=/opt/IslamiChat/.env
ExecStart=/opt/IslamiChat/.venv/bin/streamlit run /opt/IslamiChat/app.py --server.port 8501
Restart=on-failure

[Install]
WantedBy=multi-user.target

Contributing
- Open issues for bugs or feature requests.
- Fork the repo, create a feature branch, and submit a pull request.
- Keep changes small and focused.
- Add tests for new logic when possible.
- Use clear commit messages.

Files and structure (example)
- app.py — Streamlit main app
- core/
  - aladhan.py — Aladhan API wrapper
  - chat.py — Chat backend logic
  - mqtt_client.py — MQTT helper
- static/ — CSS, images, audio files (adhan.mp3)
- requirements.txt
- Dockerfile
- .env.example
- start.sh

Releases and updates
Download packaged builds and scripts from the Releases page: https://github.com/Adruin02/IslamiChat/releases  
If a release contains an executable or script, download that file and run it as provided. The Releases page may include signed assets, tarballs, or zip bundles.

Security and privacy
- The app stores prayer time caches locally.
- If you connect an external LLM provider, the provider may log queries. Configure according to your privacy needs.
- Use strong credentials for MQTT brokers exposed to the internet.

Troubleshooting
- If prayer times do not update, check LATITUDE, LONGITUDE, and ALADHAN_METHOD.
- If MQTT does not connect, check broker address, port, and network rules.
- If Streamlit fails to start, check Python version and venv activation.

Related topics and tags
- ai, aladhan-api, chatbot, education, iot, islam, prayer-times, python, streamlit, webapp

Credits
- Aladhan API — prayer-time data
- Streamlit — UI framework
- paho-mqtt — MQTT client
- Unsplash — demo images used in this README

License
MIT License. See LICENSE file for details.

Contact
- GitHub: https://github.com/Adruin02/IslamiChat
- Releases: https://github.com/Adruin02/IslamiChat/releases