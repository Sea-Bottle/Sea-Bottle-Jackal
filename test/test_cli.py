import os
import subprocess
import unittest


class TestCli(unittest.TestCase):

    def setUp(self) -> None:
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        self.img_name = "black"
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.script_file = "jackalify.py"
        self.img_path = os.path.join(self.data_dir, f"{self.img_name}.png")
        self.script_path = os.path.join(self.root_path, self.script_file)

    def test_make_img(self):
        res = subprocess.run(["python", self.script_path, self.img_path])
        self.assertEqual(0, res.returncode)
        self.assertTrue(os.path.isfile(os.path.join(self.data_dir, f"{self.img_name}_jackalified.png")))
        os.remove(os.path.join(self.data_dir, f"{self.img_name}_jackalified.png"))

        res = subprocess.run(["python", self.script_path, "-o", self.img_path, self.img_path])
        self.assertEqual(0, res.returncode)
        self.assertTrue(os.path.isfile(os.path.join(self.data_dir, f"{self.img_name}_jackalified.png")))
        os.remove(os.path.join(self.data_dir, f"{self.img_name}_jackalified.png"))

        res = subprocess.run(["python", self.script_path, "-o", "other.png", self.img_path])
        self.assertEqual(0, res.returncode)
        self.assertTrue(os.path.isfile("other.png"))
        os.remove("other.png")

    def test_make_gif(self):
        res = subprocess.run(["python", self.script_path, "-g", self.img_path])
        self.assertEqual(0, res.returncode)
        self.assertTrue(os.path.isfile(os.path.join(self.data_dir, f"{self.img_name}_jackalified.gif")))
        os.remove(os.path.join(self.data_dir, f"{self.img_name}_jackalified.gif"))

        res = subprocess.run(["python", self.script_path, "-g", "-o", "other.gif", self.img_path])
        self.assertEqual(0, res.returncode)
        self.assertTrue(os.path.isfile("other.gif"))
        os.remove("other.gif")

    def test_non_existent(self):
        non_existent_path = os.path.join(self.data_dir, "non_existing.png")
        self.assertFalse(os.path.isfile(non_existent_path))
        res = subprocess.run(["python", self.script_path, non_existent_path])
        self.assertEqual(2, res.returncode)

    def test_wrong_file(self):
        res = subprocess.run(["python", self.script_path, self.data_dir])
        self.assertEqual(2, res.returncode)

    def test_wrong_args(self):
        res = subprocess.run(["python", self.script_path])
        self.assertEqual(2, res.returncode)

        res = subprocess.run(["python", self.script_path, "-other", self.img_path])
        self.assertEqual(2, res.returncode)

        res = subprocess.run(["python", self.script_path, self.img_path, "other.png"])
        self.assertEqual(2, res.returncode)

        res = subprocess.run(["python", self.script_path, self.img_path, "-o", self.img_path, "-g"])
        self.assertEqual(2, res.returncode)

        res = subprocess.run(["python", self.script_path, "-g", self.img_path, "-o", "other.mkv"])
        self.assertEqual(2, res.returncode)

        res = subprocess.run(["python", self.script_path, self.img_path, "-w"])
        self.assertEqual(2, res.returncode)
