import requests
import json
import os
from datetime import datetime

# URL de la API SBS
API_URL = "https://api.decolecta.com/v1/tipo-cambio/sbs/average"

# Token desde variable de entorno (NO hardcodeado)
TOKEN = os.getenv("sk_12132.q5iZnBu6JWWn3R8LpbRIk0kZEWXNe2i8")

if not TOKEN:
    raise ValueError("No se encontró la variable de entorno SBS_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

response = requests.get(API_URL, headers=headers, timeout=15)
response.raise_for_status()

data = response.json()

# Estructura del registro
registro = {
    "fecha": data.get("date"),
    "compra": data.get("buy"),
    "venta": data.get("sell"),
    "fecha_registro": datetime.utcnow().isoformat()
}

# Guardar histórico en JSON Lines (1 registro por línea)
archivo = "tipo_cambio_sbs.jsonl"

with open(archivo, "a", encoding="utf-8") as f:
    f.write(json.dumps(registro, ensure_ascii=False) + "\n")

print("Registro guardado:", registro)
