import time
from functools import wraps
from prometheus_client import Counter, Gauge, Summary

# Prometheus
max_object_processing_time = Gauge('max_object_processing_time_seconds', 'Maximum time taken to process an object')
min_object_processing_time = Gauge('min_object_processing_time_seconds', 'Minimum time taken to process an object')
avg_object_processing_time = Summary('avg_object_processing_time_seconds', 'Average time taken to process an object')

max_row_processing_time = Gauge('max_row_processing_time_seconds', 'Maximum time taken to process a row')
min_row_processing_time = Gauge('min_row_processing_time_seconds', 'Minimum time taken to process a row')
avg_row_processing_time = Summary('avg_row_processing_time_seconds', 'Average time taken to process a row')

objects_processed = Counter('objects_processed', 'Cantidad de objetos procesados')
objects_error = Counter('objects_error', 'Cantidad de objetos con error')
rows_processed = Counter('rows_processed', 'Cantidad de filas procesados')
rows_error = Counter('rows_error', 'Cantidad de filas con error')

# Function used to measure the processing time of a function
def measure_object_processing_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        processing_time = time.time() - start_time
        
        # Observe the processing time
        avg_object_processing_time.observe(processing_time)
        
        # Update the max processing time
        max_object_processing_time.set(max(max_object_processing_time._value.get(), processing_time))
        
        # Update the min processing time
        # Do not let the min processing time to be 0
        if min_object_processing_time._value.get() == 0:
            min_object_processing_time.set(processing_time)
        else:
            min_object_processing_time.set(min(min_object_processing_time._value.get(), processing_time))
        
        return result
    return wrapper

def measure_row_processing_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        processing_time = time.time() - start_time
        
        # Observe the processing time
        avg_row_processing_time.observe(processing_time)
        
        # Update the max processing time
        max_row_processing_time.set(max(max_row_processing_time._value.get(), processing_time))
        
        # Update the min processing time
        # Do not let the min processing time to be 0
        if min_row_processing_time._value.get() == 0:
            min_row_processing_time.set(processing_time)
        else:
            min_row_processing_time.set(min(min_row_processing_time._value.get(), processing_time))
        
        return result
    return wrapper