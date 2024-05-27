import http.server
import random
from prometheus_client import start_http_server
from prometheus_client import Counter

REQUESTS = Counter('hello_worlds_total','Hello Worlds requested.')
EXCEPTIONS = Counter('hello_world_exceptions_total','Exceptions serving Hello World.')
SALES = Counter('hello_world_sales_euro_total','Euros made serving Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.inc()
        with EXCEPTIONS.count_exceptions():
            if random.random() < 0.2:
                raise Exception
        euros = random.random()
        SALES.inc(euros)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
        self.wfile.write("Hello World for {} euros.".format(euros).encode())

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()


# :8000/metrics -metrics for p9s:

# # HELP python_gc_objects_collected_total Objects collected during gc
# # TYPE python_gc_objects_collected_total counter
# python_gc_objects_collected_total{generation="0"} 249.0
# python_gc_objects_collected_total{generation="1"} 12.0
# python_gc_objects_collected_total{generation="2"} 0.0
# # HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# # TYPE python_gc_objects_uncollectable_total counter
# python_gc_objects_uncollectable_total{generation="0"} 0.0
# python_gc_objects_uncollectable_total{generation="1"} 0.0
# python_gc_objects_uncollectable_total{generation="2"} 0.0
# # HELP python_gc_collections_total Number of times this generation was collected
# # TYPE python_gc_collections_total counter
# python_gc_collections_total{generation="0"} 33.0
# python_gc_collections_total{generation="1"} 2.0
# python_gc_collections_total{generation="2"} 0.0
# # HELP python_info Python platform information
# # TYPE python_info gauge
# python_info{implementation="CPython",major="3",minor="12",patchlevel="0",version="3.12.0"} 1.0
# # HELP hello_worlds_total Hello Worlds requested.
# # TYPE hello_worlds_total counter
# hello_worlds_total 44.0
# # HELP hello_worlds_created Hello Worlds requested.
# # TYPE hello_worlds_created gauge
# hello_worlds_created 1.7168286785966053e+09
# # HELP hello_world_exceptions_total Exceptions serving Hello World.
# # TYPE hello_world_exceptions_total counter
# hello_world_exceptions_total 7.0
# # HELP hello_world_exceptions_created Exceptions serving Hello World.
# # TYPE hello_world_exceptions_created gauge
# hello_world_exceptions_created 1.7168286785966053e+09
# # HELP hello_world_sales_euro_total Euros made serving Hello World.
# # TYPE hello_world_sales_euro_total counter
# hello_world_sales_euro_total 19.625549830170876
# # HELP hello_world_sales_euro_created Euros made serving Hello World.
# # TYPE hello_world_sales_euro_created gauge
# hello_world_sales_euro_created 1.7168286785966053e+09