from django.conf.urls import url
from game.views import (
    VerifiyWordView,
    GameBoardView,
)

urlpatterns = [
    url(
        r'word/(?P<game_id>[0-9a-f-]+)',
        VerifiyWordView.as_view(),
        name='verify_word_view'
    ),
    url(
        r'board/(?P<user_name>[0-9a-zA-Z-]+)',
        GameBoardView.as_view(),
        name='game_board_view'
    ),
]
