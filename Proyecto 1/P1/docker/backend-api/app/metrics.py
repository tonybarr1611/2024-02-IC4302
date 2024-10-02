from prometheus_client import Counter, Gauge, Summary

# Counters for cache hits and misses
cache_hits = Counter('cache_hits_total', 'Total number of cache hits')
cache_misses = Counter('cache_misses_total', 'Total number of cache misses')

# Gauges for max and min processing time (in seconds)
max_processing_time = Gauge('max_processing_time', 'Maximum processing time in seconds')
min_processing_time = Gauge('min_processing_time', 'Minimum processing time in seconds')

# Summary for average processing time
avg_processing_time = Summary('processing_time_seconds', 'Average processing time in seconds')

# Counter for total requests per endpoint (with a label for the endpoint name)
total_requests = Counter('total_requests', 'Total HTTP requests per endpoint', ['endpoint'])
