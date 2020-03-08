import logging
import functools

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from game.helpers import (
    validate_word,
    init_board,
    update_points_and_correct_words,
)
from game.models import Game

logger = logging.getLogger('game.views')

def _generic_model_exception(target_function):

    @functools.wraps(target_function)
    def wrapper(*args, **kwargs):
        try:
            return target_function(*args, **kwargs)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return wrapper


class VerifiyWordView(APIView):

    @_generic_model_exception
    def post(self, request, *args, **kwargs):
        game_id = kwargs.get('game_id')

        submitted_word = request.POST.get('word')
        data = {
            'check': False,
        }

        if submitted_word :
            game = Game.objects.get(id=game_id)

            if validate_word(submitted_word):
                # Update the correct word and points
                game = update_points_and_correct_words(
                    game_id,
                    submitted_word,
                )

                correct_words_str = game.correct_words
                if correct_words_str:
                    correct_words = correct_words_str.split(',')
                else:
                    correct_words=[]
                
                data.update(
                    check=True,
                    points=game.points,
                    correct_words=correct_words
                )
            else:
                correct_words_str = game.correct_words
                if correct_words_str:
                    correct_words = correct_words_str.split(',')
                else:
                    correct_words=[]

                data.update(
                    check=False,
                    points=game.points,
                    correct_words=correct_words
                )

        # Call API
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class GameBoardView(APIView):

    @_generic_model_exception
    def get(self, request, *args, **kwargs):
        user_name = kwargs.get('user_name')

        board, game_id = init_board(user_name)
        data = {
            'id': game_id,
            'data': board,
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

        
