from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from game.helpers import (
    validate_word,
    update_points_and_correct_words,
    init_board,
    OXFORD_DICT_BASE_URL,
    OXFORD_DICT_ENTRY_URL,
    GAME_BOARD_SIZE,
)
from game.models import Game


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == f'{OXFORD_DICT_BASE_URL}{OXFORD_DICT_ENTRY_URL}/en-us/apple':
        return MockResponse({}, 200)
    elif args[0] == f'{OXFORD_DICT_BASE_URL}{OXFORD_DICT_ENTRY_URL}/en-us/txil':
        return MockResponse({}, 400)

    return MockResponse(None, 404)


class ValidateWordTestCases(TestCase):

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_validate_word_valid(self, mock_get):
        res = validate_word('apple')
        self.assertTrue(res)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_validate_word_invalid(self, mock_get):
        res = validate_word('txil')
        self.assertFalse(res)

class InitBoardTestCase(TestCase):

    def test_init_board(self):
        user_name='Jane Doe'
        board, uuid = init_board(user_name)
        self.assertTrue(board)
        self.assertTrue(uuid)
        self.assertEqual(len(board), GAME_BOARD_SIZE)
        self.assertEqual(len(board[0]), GAME_BOARD_SIZE)

        game = Game.objects.get(id=uuid)
        self.assertEqual(game.user_name, user_name)

class UpdatePointsAndCorrectWordsTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.game = Game.objects.create(
            points=2,
            user_name='test',
            correct_words='apple,banana'
        )

    def test_update_points_and_correct_words_success(self):
        correct_word = 'peach'
    
        game = update_points_and_correct_words(
            self.game.id,
            correct_word
        )

        self.assertEqual(game.points, 7)
        self.assertEqual(game.id, self.game.id)
        self.assertEqual(game.correct_words, 'apple,banana,peach')

    def test_update_points_and_correct_words_wrong_uuid(self):
        correct_word = 'peach'

        with self.assertRaises(Game.DoesNotExist):
            update_points_and_correct_words(
                uuid4(),
                correct_word
            )