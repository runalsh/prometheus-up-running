import http.server
from prometheus_client import start_http_server, Counter
from prometheus_client import Summary

REQUESTS = Counter('hello_worlds_total',
    'Hello Worlds requested.',
labelnames=['path', 'method'])

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.labels(self.path, self.command).inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

FETCHES = Counter('cache_fetches_total',
    'Fetches from the cache.',
labelnames=['cache'])

class MyCache(object):
    def __init__(self, name):
        self._fetches = FETCHES.labels(name)
        self._cache = {}
    def fetch(self, item):
        self._fetches.inc()
        return self._cache.get(item)
    def store(self, item, value):
        self._cache[item] = value
REQUESTS = Counter('http_requests_total',
    'HTTP requests.',
labelnames=['path'])

REQUESTS.labels('/foo')
REQUESTS.labels('/bar')

LATENCY = Summary('http_requests_latency_seconds',
    'HTTP request latency.',
labelnames=['path'])

foo = LATENCY.labels('/foo')

@foo.time()
def foo_handler(params):
    pass

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()


'''
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 249.0
python_gc_objects_collected_total{generation="1"} 12.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 33.0
python_gc_collections_total{generation="1"} 2.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="12",patchlevel="0",version="3.12.0"} 1.0
# HELP hello_worlds_total Hello Worlds requested.
# TYPE hello_worlds_total counter
hello_worlds_total{method="GET",path="/foobar"} 17.0
hello_worlds_total{method="GET",path="/favicon.ico"} 5.0
hello_worlds_total{method="GET",path="/foo+bar"} 1.0
# HELP hello_worlds_created Hello Worlds requested.
# TYPE hello_worlds_created gauge
hello_worlds_created{method="GET",path="/foobar"} 1.7168342489707448e+09
hello_worlds_created{method="GET",path="/favicon.ico"} 1.7168342492469904e+09
hello_worlds_created{method="GET",path="/foo+bar"} 1.7168342574585466e+0

'''    