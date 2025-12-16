import requests
import json
import os
from datetime import datetime

# URL de la API SBS
API_URL = "https://api.decolecta.com/v1/tipo-cambio/sbs/average"

# Token desde variable de entorno
TOKEN = os.getenv("SBS_TOKEN")

if not TOKEN:
    raise ValueError("No se encontró la variable de entorno SBS_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

response = requests.get(API_URL, headers=headers, timeout=15)
response.raise_for_status()

data = response.json()

# Estructura correcta según la API real
registro = {
    "fecha": data.get("date"),
    "compra": float(data.get("buy_price")),
    "venta": float(data.get("sell_price")),
    "moneda_base": data.get("base_currency"),
    "moneda_cotizada": data.get("quote_currency"),
    "fecha_registro": datetime.utcnow().isoformat()
}

# Guardar histórico en JSON Lines
archivo = "tipo_cambio_sbs.jsonl"

with open(archivo, "a", encoding="utf-8") as f:
    f.write(json.dumps(registro, ensure_ascii=False) + "\n")

print("Registro guardado:", registro)
