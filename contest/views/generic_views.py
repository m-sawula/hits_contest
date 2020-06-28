from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from contest.models import Album
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class AlbumIndexView(LoginRequiredMixin, ListView):
    model = Album
    template_name = "contest/panel/album/index.html"


class AlbumCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'contest.add_album'
    model = Album
    fields = ['album_name', 'author']
    template_name = "contest/panel/album/create.html"
    success_url = reverse_lazy('panel:albums:index')


class AlbumUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'contest.change_album'
    model = Album
    fields = ['album_name', 'author']
    template_name = 'contest/panel/album/edit.html'
    success_url = reverse_lazy('panel:albums:index')


class AlbumDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('contest.change_album', 'contest.delete_album')
    model = Album
    template_name = 'contest/panel/album/delete.html'
    success_url = reverse_lazy('panel:albums:index')