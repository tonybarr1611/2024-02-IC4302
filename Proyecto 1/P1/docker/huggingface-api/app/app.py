import time
from functools import wraps
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from prometheus_client import Counter, Gauge, Summary, generate_latest

model = SentenceTransformer('all-mpnet-base-v2')

# Métricas de Prometheus
request_count = Counter('app_requests_count', 'Número de requests totales')
# Gauges for max and min processing time (in seconds)
max_processing_time = Gauge('max_processing_time', 'Maximum processing time in seconds')
min_processing_time = Gauge('min_processing_time', 'Minimum processing time in seconds')

# Summary for average processing time
avg_processing_time = Summary('processing_time_seconds', 'Average processing time in seconds')

# Function used to measure the processing time of a function
def measure_processing_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        processing_time = time.time() - start_time
        
        # Observe the processing time
        avg_processing_time.observe(processing_time)
        
        # Update the max processing time
        max_processing_time.set(max(max_processing_time._value.get(), processing_time))
        
        # Update the min processing time
        # Do not let the min processing time to be 0
        if min_processing_time._value.get() == 0:
            min_processing_time.set(processing_time)
        else:
            min_processing_time.set(min(min_processing_time._value.get(), processing_time))
        
        return result
    return wrapper

# Crear la app Flask
app = Flask(__name__)

# Endpoint /encode
@app.route('/encode', methods=['POST'])
@measure_processing_time
def encode():
    request_count.inc()
    
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "El campo 'text' es obligatorio."}), 400
    
    text = data['text']
    embedding = model.encode(text).tolist()

    return jsonify({
        'text': text,
        'embedding': embedding
    })

# Endpoint /status
@app.route('/status', methods=['GET'])
@measure_processing_time
def status():
    request_count.inc()
    
    text = "El sistema está funcionando correctamente."
    
    embedding = model.encode(text).tolist()
    
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