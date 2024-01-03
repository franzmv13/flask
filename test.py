from api import app
import warnings
import unittest
class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category="DeprecationWarning")
    
    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "<p>Hello, World!</p>")

    def test_getactors(self):
        response = self.app.get("/actors")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Female" in response.data.decode("utf-8"))
if __name__ == "__main__":
    unittest.main()