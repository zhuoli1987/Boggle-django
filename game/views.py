import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from game.helpers import validate_word

logger = logging.getLogger('game.views')

class VerifiyWordView(APIView):

    def post(self, request, *args, **kwargs):
        submitted_word = request.POST.get('word')
        data = {
            'check': False,
        }

        if submitted_word:
            if validate_word(submitted_word):

                # Update the correct word and points
                data.update(
                    check=True,
                    points=1,
                )
            else:
                data = {

                }

        # Call API
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class GameBoardView(APIView):

    def get(self, request, *args, **kwargs):
        data = []
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
