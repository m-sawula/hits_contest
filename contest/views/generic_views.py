from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from contest.models import Album


# pokazuje listę albumów
class AlbumIndexView(ListView):
    model = Album
    template_name = "contest/panel/album/index.html"


# oddaje nowy album
class AlbumCreateView(CreateView):
    model = Album
    fields = ['album_name', 'author']
    template_name = "contest/panel/album/create.html"
    success_url = reverse_lazy('panel:albums:index')

# edycja albumu
class AlbumUpdateView(UpdateView):
    model = Album
    fields = ['album_name', 'author']
    template_name = 'contest/panel/album/edit.html'
    success_url = reverse_lazy('panel:albums:index')

# ​usunięcie albumu
class AlbumDeleteView(DeleteView):
    model = Album
    template_name = 'contest/panel/album/delete.html'
    success_url = reverse_lazy('panel:albums:index')
