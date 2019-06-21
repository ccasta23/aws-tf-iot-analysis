import paho.mqtt.client as mqtt #import the client1
import time
from ECC import decriptText
from ECC import cipherText
from ECC import cipherTextSimon
from ECC import cipherTextSpeck

############
def on_message(client, userdata, message):
    message =decriptText(str(message.payload.decode("utf-8")))
    print("message received " , message)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
broker_address="192.168.1.70"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","MABE")
client.subscribe("MABE")
print("Publishing message to topic","MABE")
message = cipherText('OFF')
client.publish("MABE",message)
print(decriptText(message))
time.sleep(100) # wait
client.loop_stop() #stop the loop