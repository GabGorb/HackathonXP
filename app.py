# app.py
from dotenv import load_dotenv
load_dotenv()


import os
import requests
from flask import Flask, request, jsonify
from bot import parse_command

app = Flask(__name__)

VERIFY_TOKEN = "gab123"

# Pega as credenciais do ambiente
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

WHATSAPP_API_URL = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"


def send_whatsapp_message(phone: str, text: str):
    """
    Envia uma mensagem de texto pelo WhatsApp Cloud API.
    """
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        print("ERRO: WHATSAPP_TOKEN ou WHATSAPP_PHONE_NUMBER_ID não configurados.")
        return

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": text
        }
    }

    try:
        resp = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        print("RESPOSTA WHATSAPP:", resp.status_code, resp.text)
    except Exception as e:
        print("ERRO AO ENVIAR WHATSAPP:", e)


@app.route("/", methods=["GET"])
def home():
    return "Cartola de Investimentos Bot está no ar!", 200


# Endpoint de verificação (Meta / WhatsApp Cloud API)
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Erro de verificação", 403


# Endpoint para receber mensagens
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("DEBUG RECEBIDO:", data)

    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return "EVENTO IGNORADO", 200

        message = messages[0]
        phone = message.get("from")
        text = message.get("text", {}).get("body", "")

        print(f"[{phone}] => {text}")

        # Processa comando
        reply = parse_command(phone, text)
        print(f"Bot => {reply}")

        # 🔥 Agora envia a resposta pelo WhatsApp
        send_whatsapp_message(phone, reply)

        # Retorna OK para o Webhook do Meta
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("ERRO NO WEBHOOK:", e)
        return jsonify({"error": "erro interno"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
