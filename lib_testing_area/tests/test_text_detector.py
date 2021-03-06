# -*- coding: utf-8 -*-

from .context import *

import unittest
import cv2

DEBUG = False


class test_text_detector(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.conf = configuration.Default_configuration()
        self.text_handler = text_handler.Text_handler(self.conf)
        self.test_file_path = pathlib.Path.cwd() / pathlib.Path("tests/test_files")

        if DEBUG:
            print(str(self.test_file_path))

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_load_picture_basic(self):
        simple_picture_path = self.test_file_path / "simple_text.png"
        target_picture = picture_class.Picture(id=None, conf=self.conf, path=simple_picture_path)
        self.text_handler.extract_text(target_picture)

    def test_round_32(self):
        result = self.text_handler.length_to_32_multiple(300,1)
        self.assertEqual(result,320)
        result = self.text_handler.length_to_32_multiple(300,2)
        self.assertEqual(result,160)

    def test_get_mean_colors(self):
        simple_picture_path = self.test_file_path / "simple_text.png"
        target_picture = picture_class.Picture(id=None, conf=self.conf, path=simple_picture_path)
        image = self.text_handler.picture_to_cv2_picture(target_picture)

        result = self.text_handler.get_mean_color(image, 0, 0, 100,100)
        self.assertEqual(result[0], 215)
        self.assertEqual(result[1], 120)
        self.assertEqual(result[2], 0)

        result = self.text_handler.get_mean_color(image, 200, 200, 400, 400)
        self.assertEqual(result[0], 220)
        self.assertEqual(result[1], 137)
        self.assertEqual(result[2], 32)

    def test_bincount_color(self):
        simple_picture_path = self.test_file_path / "simple_text.png"
        target_picture = picture_class.Picture(id=None, conf=self.conf, path=simple_picture_path)
        image = self.text_handler.picture_to_cv2_picture(target_picture)

        result = self.text_handler.get_hist_count_colors(image, 0, 0, 100,100)
        self.assertEqual(result[0], 215)
        self.assertEqual(result[1], 120)
        self.assertEqual(result[2], 0)

        result = self.text_handler.get_hist_count_colors(image, 200, 200, 400, 400)
        self.assertEqual(result[0], 215)
        self.assertEqual(result[1], 120)
        self.assertEqual(result[2], 0)

    def test_heavy_testing(self):
        directory = self.test_file_path.parent.parent.parent / "datasets" / "raw_phishing"
        target_dir = self.test_file_path.parent.parent.parent / "datasets" / "raw_phishing_COLORED"

        for x in directory.resolve().iterdir():
            if x.is_file():
                print(x)
                image = picture_class.Picture(id=None, conf=self.conf, path=x)
                result_image = self.text_handler.extract_text(image)
                cv2.imwrite(str(target_dir / x.name), result_image)


if __name__ == '__main__':
    unittest.main()