from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer
import sys
import os

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

if sys.argv[1:]:
    address = sys.argv[1]
    interface = '0.0.0.0'
    port = int(address)

else:
    port = 8000
    interface = '0.0.0.0'

if sys.argv[2:]:
    os.chdir(sys.argv[2])

print('Started HTTP server on ' +  interface + ':' + str(port))

handler = SimpleHTTPRequestHandler
handler.protocol_version = "HTTP/0.9"
handler.request_version = "HTTP/0.9"

server = ThreadingSimpleServer((interface, port), handler)
try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print('Stopped...')