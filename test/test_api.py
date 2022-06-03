import os
import unittest

from jackalify.app import app
from fastapi.testclient import TestClient


class TestApi(unittest.TestCase):

    def setUp(self) -> None:
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        self.client = TestClient(app)
        self.result_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                       "..", "jackalify", "static", "working"))

    def test_correct_file(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        if os.path.isfile(os.path.join(self.result_dir, 'jackalified.gif')):
            os.remove(os.path.join(self.result_dir, 'jackalified.gif'))
        if os.path.isfile(os.path.join(self.result_dir, 'jackalified.png')):
            os.remove(os.path.join(self.result_dir, 'jackalified.png'))

        with open(os.path.join(self.data_dir, f"black.png"), "rb") as f:
            files = {"file": (f.name, f, "multipart/form-data")}
            response = self.client.post("/", files=files)
            self.assertEqual(200, response.status_code)
            self.assertTrue(os.path.isfile(os.path.join(self.result_dir, 'jackalified.gif')))
            self.assertTrue(os.path.isfile(os.path.join(self.result_dir, 'jackalified.png')))

    def test_wrong_file(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        with open(os.path.join(self.data_dir, f"coloured_jackalified.gif"), "rb") as f:
            files = {"file": (f.name, f, "multipart/form-data")}
            response = self.client.post("/", files=files)
            self.assertEqual(415, response.status_code)
