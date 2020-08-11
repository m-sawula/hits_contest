"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from contest.views.standard_views import (
    CommonIndexView,
    PanelIndexView,
    AuthorIndexView,
    AuthorUpdateView,
    AuthorDeleteView,
    AuthorCreateView,
    SongIndexView,
    SongCreateView,
    SongUpdateView,
    SongDeleteView,
    LoginView,
    logout_view,
    VoteView,
    ContestSubmissionView
)

from contest.views.generic_views import (
    AlbumIndexView,
    AlbumCreateView,
    AlbumUpdateView,
    AlbumDeleteView
)
# te adresy URL są zrobione za pomocą
album_patterns = ([
    # http://127.0.0.1:8000/panel/albums/
    path('', AlbumIndexView.as_view(), name='index'),
    path('create/', AlbumCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', AlbumUpdateView.as_view(), name="edit"),
    path('<int:pk>/delete/', AlbumDeleteView.as_view(), name="delete"),

    # http://127.0.0.1:8000/panel/albums/album_id/songs/
    path('<int:album_id>/songs/', SongIndexView.as_view(), name='songs-index'),

    path('<int:album_id>/songs/create', SongCreateView.as_view(), name='songs-create'),
    # http://127.0.0.1:8000/panel/albums/album_id/songs/song_id/edit

    path('<int:album_id>/songs/<int:song_id>/edit', SongUpdateView.as_view(), name='songs-edit'),

    path('<int:album_id>/songs/<int:song_id>/delete', SongDeleteView.as_view(), name='songs-delete'),
], 'albums')

author_patterns = ([

    path('', AuthorIndexView.as_view(), name='index'),
    path('create/', AuthorCreateView.as_view(), name='create'),
    path('<int:id>/edit/', AuthorUpdateView.as_view(), name='update'),
    path('<int:id>/delete/', AuthorDeleteView.as_view(), name='delete'),
], 'authors')

panel_patterns = ([
    # główna strona dla ZALOGOWANYCH, url: http://127.0.0.1:8000/panel/
    path('', PanelIndexView.as_view(), name='index'),

    # http://127.0.0.1:8000/panel/authors/
    path('authors/', include(author_patterns)),  # zawiera ścieżki z author_patterns

    #  http://127.0.0.1:8000/panel/albums/
    path('albums/', include(album_patterns)),  # zawiera ścieżki z album_patterns
], 'panel')

urlpatterns = [
    path('admin/', admin.site.urls),

    # główna strona palikacji dla nie zalogowanych, url: http://127.0.0.1:8000
    path('', CommonIndexView.as_view(), name='common-index'),

    # główna strona dla ZALOGOWANYCH, url: http://127.0.0.1:8000/panel/
    path('panel/', include(panel_patterns)),  # zawiera ścieżki z panel_patterns

    #
    path('login/', LoginView.as_view(), name='login'),

    #
    path('logout/', logout_view, name='logout'),

    # głosowanie na piosenki, widok bez szablonu html
    path('vote/', VoteView.as_view(), name='vote'),

    # zliczanie głosów, widok bez szablonu html
    path('submission/', ContestSubmissionView.as_view(), name='submission')
]