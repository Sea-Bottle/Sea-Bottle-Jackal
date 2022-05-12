import os
import unittest

import cv2

from src.backend.jackalify import jackalify
from src.backend.seam_carve import horizontal_shrink, vertical_shrink, shrink, seam_carve


class TestBackend(unittest.TestCase):

    def setUp(self) -> None:
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        self.img_name = "small"

    def test_seam_carve(self):
        test_array = cv2.imread(os.path.join(self.data_dir, f"{self.img_name}.png"))
        derivative = test_array

        res_array = shrink(test_array, derivative)
        self.assertEqual(test_array.shape, res_array.shape)
        res_array = vertical_shrink(test_array, derivative)
        self.assertEqual(test_array.shape, res_array.shape)
        res_array = horizontal_shrink(test_array, derivative)
        self.assertEqual(test_array.shape, res_array.shape)
        res_array = seam_carve(test_array, 'horizontal')
        self.assertEqual(test_array.shape, res_array.shape)
        res_array = seam_carve(test_array, 'vertical')
        self.assertEqual(test_array.shape, res_array.shape)

    def test_jackalify(self):
        jackalify(os.path.join(self.data_dir, f"{self.img_name}.png"),
                  os.path.join(self.data_dir, f"{self.img_name}.gif"))
        self.assertTrue(os.path.isfile(os.path.join(self.data_dir, f"{self.img_name}.gif")))
        os.remove(os.path.join(self.data_dir, f"{self.img_name}.gif"))

        jackalify(os.path.join(self.data_dir, f"{self.img_name}.png"),
                  os.path.join(self.data_dir, f"{self.img_name}.gif"),
                  os.path.join(self.data_dir, f"{self.img_name}_out.png"))
        self.assertTrue(os.path.isfile(os.path.join(self.data_dir, f"{self.img_name}.gif")))
        self.assertTrue(os.path.isfile(os.path.join(self.data_dir, f"{self.img_name}_out.png")))
        os.remove(os.path.join(self.data_dir, f"{self.img_name}.gif"))
        os.remove(os.path.join(self.data_dir, f"{self.img_name}_out.png"))
