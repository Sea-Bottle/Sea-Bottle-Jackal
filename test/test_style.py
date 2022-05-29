import os
import unittest
from typing import List

import pycodestyle


class TestCodeFormat(unittest.TestCase):
    @staticmethod
    def get_files() -> List[str]:
        files = []
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        for root, _, filenames in os.walk(path):
            for file in filenames:
                if file.endswith(".py"):
                    files.append(os.path.join(root, file))

        return files

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        files = self.get_files()
        style_guide = pycodestyle.StyleGuide(ignore=["E501"])  # skip line length check
        file_check = style_guide.check_files(files)
        self.assertEqual(0, file_check.total_errors, "Some file contains errors. To skip line use # noqa")
