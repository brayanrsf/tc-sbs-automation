import requests
import json
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===============================
# CONFIGURACIÓN API
# ===============================
API_URL = "https://api.decolecta.com/v1/tipo-cambio/sbs/average"

TOKEN = os.getenv("SBS_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró SBS_TOKEN")

# ===============================
# CONFIGURACIÓN EMAIL
# ===============================
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

if not all([EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
    raise ValueError("Faltan variables de entorno de email")

# ===============================
# CONSUMO API
# ===============================
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

response = requests.get(API_URL, headers=headers, timeout=15)
response.raise_for_status()
data = response.json()

registro = {
    "fecha": data["date"],
    "compra": float(data["buy_price"]),
    "venta": float(data["sell_price"]),
    "moneda_base": data["base_currency"],
    "moneda_cotizada": data["quote_currency"],
    "fecha_registro": datetime.utcnow().isoformat()
}

# ===============================
# ENVÍO DE CORREO
# ===============================
asunto = f"Tipo de cambio SBS – {registro['fecha']}"

cuerpo = f"""
Tipo de cambio SBS ({registro['fecha']})

Compra: {registro['compra']}
Venta: {registro['venta']}

Moneda: {registro['moneda_base']} / {registro['moneda_cotizada']}
Fecha registro (UTC): {registro['fecha_registro']}
"""

msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg["Subject"] = asunto
msg.attach(MIMEText(cuerpo, "plain"))

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)

print("Correo enviado correctamente")
print("Registro:", registro)
