import time
import os
import sys
import pika
from datetime import datetime
import json
import hashlib
import json


hostname = os.getenv('HOSTNAME')
XPATH=os.getenv('XPATH')



def callback(ch, method, properties, body):
    json_object = json.loads(body)
    with open(XPATH+'/'+hashlib.md5(body).hexdigest()+'.json', 'w') as f:
        json.dump(json_object, f)
    print(" [x] Received %r" % body)

DATA=os.getenv('DATAFROMK8S')
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITMQ_PASS')
QUEUE_NAME=os.getenv('RABBITMQ_QUEUE')




credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
