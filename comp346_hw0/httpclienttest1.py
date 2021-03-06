import unittest
from comp346_hw0 import httpclient


class TestHttpClient(unittest.TestCase):
    
    def setUp(self):
        pass

    def testGetMethod(self):
        client = httpclient.HttpClient('www.shilad.com', 80);
                
        response = client.doGet('/nonExistentPage')
        self.assertEqual(response.statusCode, 404)
        self.assertEqual(response.statusMessage.lower(), 'not found')

        response = client.doGet('/index.html')
        self.assertEqual(response.statusCode, 200)
        self.assertEqual(response.statusMessage, 'OK')
        self.assertEqual(response.headers['Content-Type'], 'text/html; charset=UTF-8' )
        self.assertTrue(response.body.find('ssen@macalester.edu') > 0)
    
if __name__ == '__main__':
    unittest.main()
