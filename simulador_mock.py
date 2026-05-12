import paho.mqtt.client as mqtt
import json
import time

broker = "localhost"

topico =  "sensor/paciente/pulmao"

client = mqtt.Client()
client.connect(broker, 1883, 60)
client.loop_start()

print("Apertando o botão de pânico virtual...")
time.sleep(0.5)

payload = json.dumps({"alerta": "ON"})
info = client.publish(topico, payload)
info.wait_for_publish()

print("Alerta enviado! Verifique sua tela!")
client.loop_stop()
client.disconnect()
