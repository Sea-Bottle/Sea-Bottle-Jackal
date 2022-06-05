import os
import unittest
from copy import deepcopy

import cv2
import numpy as np

from jackalify.jackal import jackalify
from jackalify.seam_carve import horizontal_shrink, vertical_shrink, shrink, seam_carve


class TestBackend(unittest.TestCase):

    def setUp(self) -> None:
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        self.img_name = "black"

    def test_seam_carve(self):
        test_array = cv2.imread(os.path.join(self.data_dir, f"{self.img_name}.png"))
        derivative = deepcopy(test_array[:, :, 0])
        self.assertNotEqual(id(derivative), id(test_array))

        res_array = shrink(test_array, derivative)
        self.assertEqual((test_array.shape[0], test_array.shape[1] - 1, test_array.shape[2]), res_array.shape)
        res_array = vertical_shrink(test_array, derivative)
        self.assertEqual((test_array.shape[0] - 1, test_array.shape[1], test_array.shape[2]), res_array.shape)
        res_array = horizontal_shrink(test_array, derivative)
        self.assertEqual((test_array.shape[0], test_array.shape[1] - 1, test_array.shape[2]), res_array.shape)
        res_array = seam_carve(test_array, 'horizontal')
        self.assertEqual((test_array.shape[0], test_array.shape[1] - 1, test_array.shape[2]), res_array.shape)
        res_array = seam_carve(test_array, 'vertical')
        self.assertEqual((test_array.shape[0] - 1, test_array.shape[1], test_array.shape[2]), res_array.shape)

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

    def test_result(self):
        jackalify(os.path.join(self.data_dir, "coloured.png"),
                  os.path.join(self.data_dir, "coloured.gif"),
                  os.path.join(self.data_dir, "coloured_result.png"))
        test_img = cv2.imread(os.path.join(self.data_dir, "coloured_jackalified.png"))
        result_img = cv2.imread(os.path.join(self.data_dir, "coloured_result.png"))
        self.assertTrue(np.allclose(test_img, result_img))
        os.remove(os.path.join(self.data_dir, "coloured.gif"))
        os.remove(os.path.join(self.data_dir, "coloured_result.png"))
