import os
import sys
import time
import boto3
import pika
import logging
from prometheus_client import start_http_server, Counter, Gauge

# basic configuration for logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato del mensaje
    handlers=[
        logging.FileHandler("application.log"),  # Guardar los logs en un archivo llamado application.log
        logging.StreamHandler(sys.stdout)  # show logs in console
    ]
)
logger = logging.getLogger(__name__)

# Define the Prometheus metrics 
OBJECT_COUNT = Counter('s3_object_count', 'Cantidad de objetos procesados')
PROCESSING_TIME = Gauge('s3_processing_time_seconds', 'Tiempo total de procesamiento en segundos')

# Configuration  env variables
BUCKET_NAME = os.getenv('S3_BUCKET')
KEY_PREFIX = os.getenv('S3_KEY_PREFIX')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITMQ_PASS')
QUEUE_NAME=os.getenv('RABBITMQ_QUEUE')

# Validación de variables de entorno
if not all([BUCKET_NAME, KEY_PREFIX, AWS_ACCESS_KEY, AWS_SECRET_KEY]):
    logger.error("Faltan variables de entorno necesarias.")
    sys.exit(1)

# Configurar cliente de AWS S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY

)

if not s3_client:
    logger.error("Error setting S3 client.")
    sys.exit(1)

#Conexion a rabbitmq
try :
    credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
except Exception as e:
    logger.error("Error setting RabbitMQ client.")
    sys.exit(1)

# Función para listar todos los objetos en el bucket S3, de forma recursiva
def list_s3_objects(bucket, prefix):
    objects = []
    continuation_token = None
    while True:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        
        if 'Contents' in response:
            objects.extend([obj['Key'] for obj in response['Contents']])
        
        if response.get('IsTruncated'):
            continuation_token = response.get('NextContinuationToken')
        else:
            break
    
    return objects

# Función para enviar un mensaje a RabbitMQ
def send_to_rabbitmq(message):
    try:
        # Asegurarse que la cola existe
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        # Publicar el mensaje
        channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
        logger.info(f"Mensaje enviado a RabbitMQ: {message}")
    except Exception as e:
        logger.error(f"Error al enviar mensaje a RabbitMQ: {e}")

# Función principal
def main():
    logger.info(f"Listando objetos en S3 bucket '{BUCKET_NAME}' con prefijo '{KEY_PREFIX}'")
    
    start_http_server(9102)  # Inicia el servidor HTTP para Prometheus en el puerto 8000

    start_time = time.time()

    # Listar todos los objetos en el prefijo especificado
    s3_objects = list_s3_objects(BUCKET_NAME, KEY_PREFIX)
    
    # Actualizar métrica de cantidad de objetos
    OBJECT_COUNT.inc(len(s3_objects))
    
    if not s3_objects:
        logger.info("No se encontraron objetos en el bucket.")
        return
    
    # Enviar cada objeto a RabbitMQ
    for obj_key in s3_objects:
        send_to_rabbitmq(obj_key)


    end_time = time.time()
    total_time = end_time - start_time

    # Actualizar métrica de tiempo de procesamiento
    PROCESSING_TIME.set(total_time)

    logger.info(f"Tiempo total de procesamiento: {total_time:.2f} segundos")
    logger.info("Proceso completado.")
    logger.info("Stalling to keep the container running so the metrics can be scraped.")
    time.sleep(570) # 9.5 minutes should be enough for the scraping to happen

# Ejecutar el código si es el script principal
if __name__ == "__main__":
    main()