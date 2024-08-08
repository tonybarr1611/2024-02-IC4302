import time
import os
import sys
import pika

DATA=os.getenv('DATAFROMK8S')
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITMQ_PASS')
QUEUE_NAME=os.getenv('RABBITMQ_QUEUE')


hostname = os.getenv('HOSTNAME')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)


while True:
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    msg = "{\"msg\": \""+result+"\"}"
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=msg)
    print(DATA+" - " +result)
    time.sleep(1)
    
connection.close()
