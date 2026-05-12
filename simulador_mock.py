import paho.mqtt.client as mqtt
import json
import time

broker = "localhost"

topico =  "sensor/paciente/pulmao"

client = mqtt.Client()
client.connect(broker, 1883, 60)
client.loop_start()

print("Apertando o botão de pânico virtual em 3 segundos...")
time.sleep(3)

payload = json.dumps({"alerta": "ON"})
info = client.publish(topico, payload)
info.wait_for_publish()

print("Alerta enviado! Verifique sua tela!")
client.loop_stop()
client.disconnect()
