import unittest
import json

from comp346_hw0 import httpclient
from comp346_hw0 import httpclienttest2

class TestHttpClient(httpclienttest2.TestHttpClient):

    def testPostWithParams(self):
        client = httpclient.HttpClient('httpbin.org')
        response = client.doPostWithParams('/post', {'Foo' : 'Bar'})
        data = json.loads(response.body)
        print(data)
        self.assertEqual(data['form']['Foo'], 'Bar')

    def testGetWithParams(self):
        client = httpclient.HttpClient('httpbin.org')
        response = client.doGetWithParams('/get', {'Foo' : 'Bar', 'foo' : 'bar'})
        data = json.loads(response.body)
        self.assertEqual(data['args'], {'Foo' : 'Bar', 'foo' : 'bar'})
    
    def testGetParamEncoding(self):
        client = httpclient.HttpClient('httpbin.org')
        response = client.doGetWithParams('/get', {'$foo' : 'bar &z' })

        data = json.loads(response.body)
        self.assertEqual(data['args'], {'$foo' : 'bar &z' })
    
if __name__ == '__main__':
    unittest.main()
