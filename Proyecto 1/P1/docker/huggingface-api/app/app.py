from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from prometheus_client import Counter, Histogram, start_http_server
import time

# Inicializamos el modelo Hugging Face
model = SentenceTransformer('all-mpnet-base-v2')

# Métricas de Prometheus
REQUEST_COUNT = Counter('app_requests_count', 'Número de requests totales')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Latencia de requests')

# Iniciar Prometheus en el puerto 8000
start_http_server(8000)

# Crear la app Flask
app = Flask(__name__)

# Endpoint /encode
@app.route('/encode', methods=['POST'])
def encode():
    REQUEST_COUNT.inc()
    
    start_time = time.time()
    
    # Obtener el texto del cuerpo de la solicitud
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "El campo 'text' es obligatorio."}), 400
    
    text = data['text']
    
    # Generar el embedding utilizando Hugging Face
    embedding = model.encode(text).tolist()
    
    # Calcular latencia
    REQUEST_LATENCY.observe(time.time() - start_time)
    print(text)
    # Retornar el texto y el embedding
    return jsonify({
        'text': text,
        'embedding': embedding
    })

# Endpoint /status
@app.route('/status', methods=['GET'])
def status():
    REQUEST_COUNT.inc()
    
    start_time = time.time()
    
    # Texto quemado
    text = "El sistema está funcionando correctamente."
    
    # Generar el embedding
    embedding = model.encode(text).tolist()
    
    REQUEST_LATENCY.observe(time.time() - start_time)
    print(text)
    return jsonify({
        'text': text,
        'embedding': embedding
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
