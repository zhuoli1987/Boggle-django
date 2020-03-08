from django.conf.urls import url
from game.views import (
    VerifiyWordView,
    GameBoardView,
)

urlpatterns = [
    url(
        r'word',
        VerifiyWordView.as_view(),
        name='verify_word_view'
    ),
    url(
        r'board',
        GameBoardView.as_view(),
        name='game_board_view'
    ),
]
