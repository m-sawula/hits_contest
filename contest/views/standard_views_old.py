from django.shortcuts import render, redirect
from django.views import View

from contest.forms.model_forms import SongForm
from contest.forms.standard_forms import AuthorForm
from contest.models import Author, Song, Album
from django.contrib.auth.mixins import LoginRequiredMixin


class CommonIndexView(View):
    def get(self, request):
        return render(request, "contest/common/index.html")
#     modyfikacja 11:10

# wymuszanie logowania w Django (dana sekcja nie  będzie dostępna bez zalogownaia)
# 16:40 dekoratory okalają funkcję i zmieniają wynik fukcji


class PanelIndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "contest/panel/index.html")


# 13:15
class AuthorIndexView(View):
    def get(self, request):
        return render(
            request,
            "contest/panel/author/index.html",
            {"authors": Author.objects.all().order_by("band_name")}
        )

# crud autora obsłużony jest przez standardowe vieusy i formularze
class AuthorCreateView(View):
    def get(self, request):
        form = AuthorForm()
        return render(
            request,
            "contest/panel/author/create.html",
            {"form": form}
        )

    def post(self, request):
        form = AuthorForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "contest/panel/author/create.html",
                {"form": form}
            )
        Author.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            band_name=form.cleaned_data['band_name'],
            birth_date=form.cleaned_data['birth_date'],
            debut=form.cleaned_data['debut'],
        )
        return redirect('panel:authors:index')


# 14:58 dorobić walidację patrz zdjęcie
class AuthorUpdateView(View):
    def get(self, request, id):
        author = Author.objects.get(id=id)
        form = AuthorForm({
            "fist_name": author.first_name,
            "last_name": author.last_name,
            "birth_date": author.birth_date,
            "band_name": author.band_name,
            "debut": author.debut
        })
        return render(request, 'contest/panel/author/edit.html', {
            "form": form,
            "author": author
        })

    def post(self, request, id):
        author = Author.objects.get(id=id)
        form = AuthorForm(request.POST)
        if form.is_valid():
            author.first_name = form.cleaned_data['first_name']
            author.last_name = form.cleaned_data['last_name']
            author.birth_date = form.cleaned_data['birth_date']
            author.band_name = form.cleaned_data['band_name']
            author.debut = form.cleaned_data['debut']
            author.save()
            return redirect('panel:authors:index')


class AuthorDeleteView(View):
    def get(self, request, id):
        author = Author.objects.get(id=id)
        if author:
            author.delete()
            return redirect('panel:authors:index')
        return redirect('panel:authors:index')

# 9:20
class SongIndexView(View):
    def get(self, request, album_id):
        # rozwiązanie naj mniej obciążające aplikację
        # pobrać model i model nadrzędny w tym przypadku piosenkę i album
        songs = Song.objects.filter(album_id=album_id)
        album = Album.objects.get(id=album_id)
        return render(
            request,
            "contest/panel/song/index.html",
            {"songs": songs, "album": album}
        )

# class SongCreateView(View):
#     def get(self, request, album_id):
#         # tworzenie nowej piosenk obsługiane jest przez modelForm
#         form = SongForm()
#         album = Album.objects.get(id=album_id)
#         return render(
#             request,
#             "contest/panel/song/create.html",
#             {"form": form, "album": album}
#         )
#     # 10:10 zapisywanie danych z modelForma wygląda inaczej
#     # zapisaywanie standardoewe na zdjęciu 10:11
#     # trzeba oszukać Django modelForm 10:12 nigdzie nie jest to opisane
#     # commit = False
#     def post(self, request, album_id):
#         form = SongForm(request.POST)
#         album = Album.objects.get(id=album_id)
#         if form.is_valid():
#             # tym poleceniem wyłączamy zapisywanie danych z formularza 10:20
#             # obiekt sobie czeka w pamięci do czasu zaktualizowania danych
#             # powstaje obiek (piosenka) bez jego zapisnia dodbazy
#             song = form.save(commit=False)
#             # do piosenki dodajem album
#             song.album_id = album_id
#             # i doiero teraz zapisujemy całosc
#             song.save()
#             return redirect('panel:albums:songs-index', album_id=album_id)
#         return render(
#             request,
#             "contest/panel/song/create.html",
#             {"form": form, "album": album}
#         )
class SongCreateView(View):
    def get(self, request, album_id):
        form = SongForm()
        album = Album.objects.get(id=album_id)
        return render(
            request,
            "contest/panel/song/create.html",
            {"form": form, "album": album}
        )

    def post(self, request, album_id):
        form = SongForm(request.POST)
        album = Album.objects.get(id=album_id)

        if form.is_valid():
            song = form.save(commit=False) # song = Song("nazwa", "rok", "ytLink")
            song.album_id = album.id # song = Song("nazwa", "rok", "ytLink", "album")
            song.save() # song.save to db
            return redirect('panel:albums:songs-index', album_id=album.id)
        return render(
            request,
            "contest/panel/song/create.html",
            {"form": form, "album": album}
        )

    # 10:30
    # class SongUpdateView(View):
    #     def get(self,request, album_id, song_id):
    #         song = Song.objects.filter(album_id=album_id)
    #         album = Album.objects.get(id=album_id)
    #         # potrzebny jes request post i instanece
    #         form = SongForm(request.POST)
    #         return render(
    #             request,
    #             "contest/panel/song/edit.html",
    #             {"form": form, "album": album, "song": song}
    #         )
    #     # 10:50 Marcin przy edycji nie trzeba robić haka
    #     def post(self, request):
    #         pass

class SongEditView(View):
    def get(self, request, album_id, song_id):
        album = Album.objects.get(pk=album_id)
        song = Song.objects.get(pk=song_id)
        form = SongForm(instance=song)
        return render(
            request,
            "contest/panel/song/edit.html",
            {
                "form": form,
                "song": song,
                "album": album,
            }
        )

    def post(self, request, album_id, song_id):
        album = Album.objects.get(pk=album_id)
        song = Song.objects.get(pk=song_id)
        form = SongForm(request.POST, instance=song)
        if not form.is_valid():
            return render(
                request,
                "contest/panel/song/edit.html",
                {
                    "form": form,
                    "song": song,
                    "album": album,
                }
            )
        form.save()
        return redirect('panel:albums:songs-index', album_id=album_id)


class SongDeleteView(View):
    def get(self, request, album_id, song_id):
        song = Song.objects.get(id=song_id)
        if song:
            song.delete()
        return redirect('panel:albums:songs-index', album_id=album_id)