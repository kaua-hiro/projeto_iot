import asyncio
import json
import uvicorn
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from databases import Database

DB_URL = "postgresql://iotuser:iotpass@localhost:5433/iotasma"

app = FastAPI()
database = Database(DB_URL)

# Configurando o MQTT
mqtt_config = MQTTConfig(host="localhost", port=1883)
fast_mqtt = FastMQTT(config=mqtt_config)
fast_mqtt.init_app(app)

# Variável em memória para o flet consultar
estado_atual = {"status": "Monitorando", "ultimo_alerta": None}

@app.on_event("startup")
async def startup():
    # Conectando no banco
    await database.connect()

    # Criando a tabela
    query = """
    CREATE TABLE IF NOT EXISTS alertas (
        id SERIAL PRIMARY KEY,
        paciente_id VARCHAR(50),
        status VARCHAR(50),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    await database.execute(query)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Backend escutando MQTT
@fast_mqtt.subscribe("sensor/paciente/pulmao")
async def processar_alerta(client, topic, payload, qos, properties):
    global estado_atual
    
    # Decodificando o payload que vem em bytes
    try:
        mensagem = json.loads(payload.decode())
    except Exception:
        # Fallback caso a mensagem não seja um JSON válido
        mensagem = {"alerta": payload.decode()}
        
    print(f"Mensagem recebida do ESP32: {mensagem}")

    status = mensagem.get("alerta", "OK")

    # Atualizando a memória
    if status == "ON":
        estado_atual["status"] = "EMERGÊNCIA"

    # Salvando no banco TSDB
    query = "INSERT INTO alertas (paciente_id, status) VALUES (:paciente_id, :status)"
    values = {"paciente_id": "paciente_01", "status": status}
    await database.execute(query=query, values=values)

# Rota para o Flet ver o status
@app.get("/status")
async def get_status():
    return estado_atual

# Rota para o responsável desativar alarme
@app.post("/reset")
async def reset_status():
    global estado_atual
    estado_atual["status"] = "Monitorando"
    return {"message": "Sistema resetado"}

# Inicia o servidor automaticamente
if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)