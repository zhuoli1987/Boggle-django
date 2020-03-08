import requests
import logging

from rest_framework import status
from django.conf import settings
from typing import List

OXFORD_DICT_BASE_URL = 'https://od-api.oxforddictionaries.com/api/v2/'
OXFORD_DICT_ENTRY_URL = 'entries'

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


def init_board() -> List[List[str]]:
    """
    """
    pass
