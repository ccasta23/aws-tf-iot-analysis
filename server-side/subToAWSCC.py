'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import db

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

    if useWebsocket and certificatePath and privateKeyPath:
        parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
        exit(2)

    if not useWebsocket and (not certificatePath or not privateKeyPath):
        parser.error("Missing credentials for authentication.")
        exit(2)

    # Port defaults
    if useWebsocket and not port:  # When no port override for WebSocket, default to 443
        port = 443
    if not useWebsocket and not port:  # When no port override for non-WebSocket, default to 8883
        port = 8883


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
    print("Suscribiendo a " + topic)
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
    print("Suscrito a " + topic)
    time.sleep(2)


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    data = json.loads(message.payload)
    db.crear_datos(data)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

readConfig()
initAWSConn()

while True:
    time.sleep(1)