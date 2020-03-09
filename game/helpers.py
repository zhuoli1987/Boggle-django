import requests
import logging
import random
import string

from uuid import UUID
from rest_framework import status
from django.conf import settings
from django.db import transaction

from game.models import Game
from typing import (
    List,
    Union,
    Tuple,
)

OXFORD_DICT_BASE_URL = 'https://od-api.oxforddictionaries.com/api/v2/'
OXFORD_DICT_ENTRY_URL = 'entries'
GAME_BOARD_SIZE = 4

logger = logging.getLogger('game.helpers')


def validate_word(word: str) -> bool:
    """ 
        Validate word against the Oxford
        Dictionary API. For more information:

        https://developer.oxforddictionaries.com/documentation/getting_started
    """
    if word:
        url = f'{OXFORD_DICT_BASE_URL}{OXFORD_DICT_ENTRY_URL}/en-us/{word.lower()}'
        headers = {
            'app_id': settings.OXFORD_APP_ID,
            'app_key': settings.OXFORD_API_KEY,
        }

        logger.info(f'validating {word} against oxford dictionary...')
        response = requests.get(
            url,
            headers=headers,
        )

        if response.status_code == status.HTTP_200_OK:
            return True
        else:
            return False

    return False


def init_board(user_name:str) -> Tuple[List[List[str]], str]:
    """
        Initialize the board with a 
        2-D list of random characters

        Return - 2-D list and game id
    """
    game = Game.objects.create(user_name=user_name)

    board = []

    for _ in range(GAME_BOARD_SIZE):
        row = []
        for _ in range(GAME_BOARD_SIZE):
            random_letter = random.choice(string.ascii_uppercase)
            row.append(random_letter)
        board.append(row)

    return board, game.id


@transaction.atomic()
def update_points_and_correct_words(game_id: Union[UUID, str], correct_word: str) -> Game:
    """
        Update points and the correct words list for a 
        given Game object
    """
    game = Game.objects.select_for_update().get(id=game_id)

    if correct_word:
        points = game.points
        game.points = points + len(correct_word)

        correct_words_str = game.correct_words
        if correct_words_str:
            correct_words = correct_words_str.split(',')
        else:
            correct_words=[]

        correct_words.append(correct_word)
        correct_words_str = ','.join(correct_words)
        game.correct_words = correct_words_str

        game.save()

    return game
