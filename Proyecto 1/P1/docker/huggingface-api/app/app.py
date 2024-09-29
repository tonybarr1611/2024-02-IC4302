import time
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from prometheus_client import Counter, Histogram, generate_latest

model = SentenceTransformer('all-mpnet-base-v2')

# Métricas de Prometheus
request_count = Counter('app_requests_count', 'Número de requests totales')
request_latency = Histogram('app_request_latency_seconds', 'Latencia de requests')

# Crear la app Flask
app = Flask(__name__)

# Endpoint /encode
@app.route('/encode', methods=['POST'])
def encode():
    request_count.inc()
    start_time = time.time()
    
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "El campo 'text' es obligatorio."}), 400
    
    text = data['text']
    embedding = model.encode(text).tolist()
    
    request_latency.observe(time.time() - start_time)
    return jsonify({
        'text': text,
        'embedding': embedding
    })

# Endpoint /status
@app.route('/status', methods=['GET'])
def status():
    request_count.inc()
    start_time = time.time()
    
    text = "El sistema está funcionando correctamente."
    
    embedding = model.encode(text).tolist()
    
    request_latency.observe(time.time() - start_time)
    print(text)
    return jsonify({
        'text': text,
        'embedding': embedding
    })

@app.route('/metrics')
def metrics():
    return generate_latest()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)