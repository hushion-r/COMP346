import json
import unittest
from comp346_hw0 import httpclient
from comp346_hw0 import httpclienttest1

class TestHttpClient(httpclienttest1.TestHttpClient):
    
    def testPostMethod(self):
        client = httpclient.HttpClient('httpbin.org')
        response = client.doPost('/post', 'Foo=Bar')
        data = json.loads(response.body)
        self.assertEqual(data['form']['Foo'], 'Bar')
    
if __name__ == '__main__':
    unittest.main()
