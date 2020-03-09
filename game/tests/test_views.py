from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from game.models import Game
from uuid import uuid4

class VerifyWordViewTestCase(APITestCase):

    @patch('game.views.validate_word')
    def test_verify_word_success(
        self,
        mock_validate_word,
    ):
        game = Game.objects.create(
            user_name='test',
            correct_words=None
        )

        mock_validate_word.return_value = True
        data = {
            'word': 'apple'
        }

        response = self.client.post(
            reverse(
                'verify_word_view',
                kwargs={
                    'game_id' : str(game.id)
                }
            ),
            data
        )

        self.assertTrue(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['check'], True)
        self.assertEqual(response.data['points'], 5)
        self.assertEqual(response.data['correct_words'][0], 'apple')

    @patch('game.views.validate_word')
    def test_verify_word_fail(
        self,
        mock_validate_word,
    ):
        game = Game.objects.create(
            user_name='test',
            correct_words=None
        )

        mock_validate_word.return_value = False

        data = {
            'word': 'aptte'
        }

        response = self.client.post(
            reverse(
                'verify_word_view',
                kwargs={
                    'game_id' : str(game.id)
                }
            ),
            data
        )

        self.assertTrue(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['check'], False)
        self.assertEqual(response.data['points'], 0)
        self.assertEqual(response.data['correct_words'], [])

    def test_verify_word_not_found(self):
        data = {
            'word': 'aptte'
        }

        response = self.client.post(
            reverse(
                'verify_word_view',
                kwargs={
                    'game_id' : str(uuid4())
                }
            ),
            data
        )

        self.assertTrue(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GameBoardViewTestCase(APITestCase):

    def test_init_board_success(self):
        response = self.client.get(
            reverse(
                'game_board_view',
                kwargs={
                    'user_name' : 'test name'
                }
            )
        )

        self.assertTrue(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['id'])
        self.assertTrue(response.data['data'])
    
    @patch('game.views.init_board', side_effect=Exception())
    def test_init_board_fail(self, mock_init):
        response = self.client.get(
            reverse(
                'game_board_view',
                kwargs={
                    'user_name' : 'test name'
                }
            )
        )

        self.assertTrue(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
