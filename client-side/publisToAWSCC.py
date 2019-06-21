#import basicPubSub
import os
import sys
import AWSIoTPythonSDK
sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

host = ""
rootCAPath = ""
certificatePath = ""
privateKeyPath = ""
port = 0
useWebsocket = False
clientId = ""
topic = ""
myAWSIoTMQTTClient = None

def readConfig():
    print("Iniciando Lecura de la configuración")
    with open('config.json') as json_file:  
        args = json.load(json_file)
        global host, rootCAPath, certificatePath, privateKeyPath, port, useWebsocket, clientId, topic
        host = args['host']
        rootCAPath = args['rootCAPath']
        certificatePath = args['certificatePath']
        privateKeyPath = args['privateKeyPath']
        port = args['port']
        useWebsocket = args['useWebsocket']
        clientId = args['clientId']
        topic = args['topic']
    print("Configuración cargada correctamente")

def initAWSConn():
    global host, rootCAPath, certificatePath, privateKeyPath, port, useWebsocket, clientId, topic, myAWSIoTMQTTClient
    if useWebsocket:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
    else:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()

def publishToAWS(messageReceived):
    global myAWSIoTMQTTClient
    message = {}
    message['message'] = messageReceived
    message['sequence'] = "test"
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Publicado topic: %s: %s\n' % (topic, messageJson))

readConfig()
initAWSConn()