from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class VerifiyWordView(APIView):

    def post(self, request, *args, **kwargs):
        submitted_word = request.POST.get('word')
        data = {}

        if submitted_word:
            pass

        # Call API
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class GameBoardView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_200_OK
        )
