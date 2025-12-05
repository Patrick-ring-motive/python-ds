import http.client


class HTTPResponse:
    """A mock HTTPResponse class compatible with urllib responses."""
    
    def __init__(self, url, status=200, headers=None, body=b"", reason="ok"):
        self.url = url
        self.status = status
        self.headers = headers if headers is not None else {}
        self.body = body
        self.reason = reason
        self.debuglevel = 0
        self.closed = True
        self.msg = self.headers
        self.version = "HTTP/1.1"
    
    def geturl(self):
        """Return the URL of the response."""
        return self.url
    
    def getcode(self):
        """Return the HTTP status code."""
        return self.status
    
    def getheaders(self):
        """Return the headers as a list of tuples."""
        return list(self.headers.items())
    
    def info(self):
        """Return the headers."""
        return self.headers
    
    def getheader(self, name, default=None):
        """Get a specific header value."""
        return self.headers.get(name, default)
    
    def read(self, amt=None):
        """Read and return the response body."""
        if amt is None:
            return self.body
        return self.body[:amt]
    
    def readinto(self, b):
        """Read response body into a buffer."""
        data = self.body[:len(b)]
        b[:len(data)] = data
        return len(data)


def _fetch(url, options=None):
    """Internal fetch function that makes the HTTP request."""
    if options is None:
        options = {}
    
    url = str(url)
    method = str(options.get('method', 'GET')).upper()
    body = options.get('body')
    headers = options.get('headers', {})
    
    # Parse URL to get host and path
    host = url.split('/')[2]
    path = host.join(url.split(host)[1:])
    print(path)
    
    # Make the connection
    connection = http.client.HTTPSConnection(host)
    connection.request(method, path, body=body, headers=headers)
    response = connection.getresponse()
    
    # Add missing attributes to make it compatible
    if not hasattr(response, 'url'):
        response.url = url
    
    if not hasattr(response, 'geturl'):
        def geturl():
            return url
        response.geturl = geturl
    
    if not hasattr(response, 'info'):
        def info():
            return response.headers
        response.info = info
    
    if not hasattr(response, 'getcode'):
        def getcode():
            return response.status
        response.getcode = getcode
    
    return response


def fetch(url, options=None):
    """
    Fetch a URL with error handling.
    
    Args:
        url: The URL to fetch
        options: Optional dict with 'method', 'body', 'headers'
    
    Returns:
        An HTTPResponse object (either real or mock)
    """
    if options is None:
        options = {}
    
    try:
        res = _fetch(url, options=options)
    except Exception as e:
        # Return a mock error response
        res = HTTPResponse(
            url, 
            status=569, 
            body=str(e).encode('utf-8'), 
            reason=str(e)
        )
    
    # Wrap the read method with error handling
    original_read = res.read
    
    def safe_read(amt=None):
        try:
            return original_read(amt) if amt is not None else original_read()
        except Exception as e:
            return str(e).encode('utf-8')
    
    res._read = safe_read
    return res
