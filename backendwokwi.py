import json
import uvicorn
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from databases import Database

DB_URL = "postgresql://iotuser:iotpass@localhost:5433/iotasma"

app = FastAPI()
database = Database(DB_URL)

# Broker público - o mesmo que o ESP32 no Wokwi vai usar
mqtt_config = MQTTConfig(host="broker.hivemq.com", port=1883)
fast_mqtt = FastMQTT(config=mqtt_config)
fast_mqtt.init_app(app)

# Estado em memória que o frontend consulta
estado_atual = {"status": "Monitorando", "ultimo_alerta": None}


@app.on_event("startup")
async def startup():
    await database.connect()
    query = """
        CREATE TABLE IF NOT EXISTS alertas (
            id SERIAL PRIMARY KEY,
            paciente_id VARCHAR(50),
            status VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    await database.execute(query)
    print("✅ Backend Wokwi iniciado! Aguardando mensagens do ESP32...")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    print(f"✅ Conectado ao broker HiveMQ! Código: {rc}")
    fast_mqtt.client.subscribe("sensor/paciente/pulmao")


@fast_mqtt.subscribe("sensor/paciente/pulmao")
async def processar_alerta(client, topic, payload, qos, properties):
    global estado_atual

    try:
        mensagem = json.loads(payload.decode())
    except Exception:
        mensagem = {"alerta": payload.decode()}

    print(f"📡 Mensagem recebida do ESP32 (Wokwi): {mensagem}")
    status = mensagem.get("alerta", "OK")

    if status == "ON":
        estado_atual["status"] = "EMERGÊNCIA"
        estado_atual["ultimo_alerta"] = str(__import__("datetime").datetime.now())
        query = "INSERT INTO alertas (paciente_id, status) VALUES (:paciente_id, :status)"
        values = {"paciente_id": "paciente_01", "status": status}
        await database.execute(query=query, values=values)
        print("🚨 EMERGÊNCIA registrada no banco!")


@app.get("/status")
async def get_status():
    return estado_atual


@app.post("/reset")
async def reset_status():
    global estado_atual
    estado_atual["status"] = "Monitorando"
    estado_atual["ultimo_alerta"] = None
    return {"message": "Sistema resetado"}


# ✅ CORREÇÃO CRÍTICA: o nome aqui deve ser "backendwokwi:app", não "backend:app"
if __name__ == "__main__":
    uvicorn.run("backendwokwi:app", host="0.0.0.0", port=8000, reload=True)