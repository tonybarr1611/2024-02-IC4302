from prometheus_client import Counter, Gauge, Summary

# Gauges for max and min processing time (in seconds)
max_processing_time = Gauge('ba_max_processing_time', 'Maximum processing time in seconds')
min_processing_time = Gauge('ba_min_processing_time', 'Minimum processing time in seconds')

# Summary for average processing time
avg_processing_time = Summary('ba_processing_time_seconds', 'Average processing time in seconds')

# Counter for total requests per endpoint (with a label for the endpoint name)
total_requests = Counter('ba_total_requests', 'Total HTTP requests per endpoint', ['endpoint'])
