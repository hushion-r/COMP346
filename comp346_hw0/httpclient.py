import socket
import string
import urllib
import urllib.parse

# author: Rae Hushion
# COMP 346 - 01
#
# worked with Jeremy
# went to study sessions

class HttpResponse:
    """
        Holds a structured http response.
        You will be responsible for translating an http response
        string into this structure.
    """
    def __init__(self):
        self.statusCode = 200
        self.statusMessage = 'OK'
        self.headers = {}
        self.body = ''

    def __repr__(self):
        return (
                'status=%s headers=%s body=%s...' %
                (self.statusCode, self.headers, self.body)
            )


class HttpClient:
    def __init__(self, host, port=80):
        """Constructs a new http client."""
        self.host = host
        self.port = port
    
    def doGet(self, path):
        """
            Executes an HTTP GET method and returns the result
            as an HttpResponse object.
        """
        sock = self._writeRequest(self._constructGetRequest(path))
        result = self._readResponse(sock)
        sock.close()
        return result
        
    def doPost(self, path, body):
        """
            Executes an HTTP POST method and returns the result
            as an HttpResponse object.
        """
        sock = self._writeRequest(self._constructPostRequest(path, body))
        result = self._readResponse(sock)
        sock.close()
        return result

    
    def doGetWithParams(self, path, params):
        """
            Executes an HTTP GET method and returns the result
            Params should be a dictionary of unencoded query parameters
            as an HttpResponse object.
        """
        URLEncodedParams = "?"
        for items in params:
            URLEncodedParams += urllib.parse.quote_plus(items) + "=" + urllib.parse.quote_plus(params[items]) + "&"
        URLEncodedParams = URLEncodedParams[0:-1]
        return self.doGet(path+URLEncodedParams)
    
    def doPostWithParams(self, path, params):
        """
            Executes an HTTP POST method and returns the result
            Params should be a dictionary of unencoded query parameters
            as an HttpResponse object.
        """
        URLEncodedParams = ""
        for items in params:
            URLEncodedParams += urllib.parse.quote_plus(items) + "=" + urllib.parse.quote_plus(params[items]) + "&"
        URLEncodedParams = URLEncodedParams[0:-1]
        return self.doPost(path, URLEncodedParams)
    
    def _constructGetRequest(self, path):
        """
            Returns a string containing an HTTP 1.0 GET request
            for self.host and the requested path.
        """
        request = "GET " + path + " HTTP/1.0\r\n"\
                  + "Host: " + self.host + "\r\n\r\n"
        return request
    
    def _constructPostRequest(self, path, body):
        """
            Returns a string containing an HTTP 1.0 GET request
            for self.host and the requested path and body.
        """
        postRequest = "POST " + path + " HTTP/1.0\r\n"\
                      + "Host: " + self.host + "\r\n" \
                      + "Content-Type: application/x-www-form-urlencoded\r\n" \
                      + "Content-Length: " + str(len(body)) + "\r\n\r\n" \
                      + body + "\r\n\r\n"
        return postRequest
    
    def _writeRequest(self, request):
        """
            Creates a socket connected to the host and port
            Writes the request out and returns the socket object.
        """
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(request.encode('utf-8'))
        return s
    
    def _readResponse(self, sock):
        """
            Reads in a response from a socket object.
            Returns a filled-in HttpResponse object.
        """
        responseLines = self._readResponseStr(sock).split('\r\n')
        response = HttpResponse()
        response.headers["Host"] = self.host    # necessary?
        response.statusCode = int(responseLines[0][9:12])
        response.statusMessage = responseLines[0][13:]
        for items in responseLines:
            if ":" in items:
                headerAndInfo = items.split(": ")
                response.headers[headerAndInfo[0]] = headerAndInfo[1]
        response.body = responseLines[-1]
        return response 
    
    def _readResponseStr(self, sock):
        """
            Reads in a response from a socket object.
            Returns the string contents of the response.
        """
        # Reads the response.
        # Since we are using HTTP 1.0, we can read until EOF
        bytesRead = 'foo'
        response = ''        
        while len(bytesRead) > 0: 
            bytesRead = sock.recv(1024)
            response += bytesRead.decode('utf-8')
        return response    
    
if __name__ == '__main__':
    client1 = HttpClient('www.npr.org')
    print(client1.doGet('/index.html'))
    client1 = HttpClient('webapps.macalester.edu')
    print(client1.doPost('/directory/search.cfm', 'Name=kyle'))
