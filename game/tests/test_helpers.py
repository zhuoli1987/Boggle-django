from unittest import TestCase
from unittest.mock import patch

from game.helpers import validate_word

class ValidateWordTestCases(TestCase):

    def test_validate_word_valid(self):
        res = validate_word('apple')
        self.assertTrue(res)

    def test_validate_word_invalid(self):
        res = validate_word('txil')
        self.assertFalse(res)

    def test_validate_word_api_error(self):
        pass