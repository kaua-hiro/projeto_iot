import paho.mqtt.publish as publish
import json

print("🚀 Disparando o botão de pânico virtual...")

payload = json.dumps({"alerta": "ON"})
# Essa função conecta, manda o alerta e desconecta na mesma hora
publish.single("sensor/paciente/pulmao", payload, hostname="broker.hivemq.com")

print("💥 Alerta de EMERGÊNCIA enviado para a nuvem!")