import unittest
import requests

class TestEmployeeAPI(unittest.TestCase):
    
    base_url = "http://localhost:8080/api/v1"
    
    def test_get_employees(self):
        response = requests.get(f"{self.base_url}/employees")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    

if __name__ == "__main__":
    test_order = ["test_get_employees"] # important so the delete test will work
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
    unittest.main(testLoader=loader, verbosity=2)
