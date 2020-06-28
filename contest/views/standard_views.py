from django.shortcuts import render, redirect
from django.views import View
from contest.models import Author, Song, Album
from contest.forms.standard_forms import AuthorForm, LoginForm
from contest.forms.model_forms import SongForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class LoginView(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect('panel:index')

        return render(
            request,
            "contest/auth/login.html",
            {"form": LoginForm()}
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "contest/auth/login.html",
                {"form": form}
            )

        user = authenticate(
            request=request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )  # fetch user object

        if user is None:
            messages.add_message(request, messages.WARNING, 'User does not exist in database!')
            return redirect('login')
        login(request, user)  # session file and cookie
        messages.add_message(request, messages.SUCCESS, 'User logged in successfully')
        return redirect('panel:index')


@login_required
def logout_view(request):
    logout(request)
    return redirect('common-index')


class CommonIndexView(View):
    def get(self, request):
        return render(
            request,
            "contest/common/index.html",
            {"songs": Song.objects.all().order_by('sort_order')}
        )


class PanelIndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "contest/panel/index.html")


class AuthorIndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            "contest/panel/author/index.html",
            {"authors": Author.objects.all().order_by("band_name")}
        )


class AuthorCreateView(LoginRequiredMixin, View):
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


class AuthorUpdateView(LoginRequiredMixin, View):
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
        if not form.is_valid():
            return render(request, 'contest/panel/author/edit.html', {
                "form": form,
                "author": author
            })

        author.first_name = form.cleaned_data['first_name']
        author.last_name = form.cleaned_data['last_name']
        author.birth_date = form.cleaned_data['birth_date']
        author.band_name = form.cleaned_data['band_name']
        author.debut = form.cleaned_data['debut']
        author.save()
        return redirect('panel:authors:index')


class AuthorDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        author = Author.objects.get(id=id)
        if author:
            author.delete()
            return redirect('panel:authors:index')
        return redirect('panel:authors:index')


class SongIndexView(LoginRequiredMixin, View):
    def get(self, request, album_id):
        songs = Song.objects.filter(album_id=album_id)
        album = Album.objects.get(id=album_id)
        return render(
            request,
            "contest/panel/song/index.html",
            {"songs": songs, "album": album}
        )


class SongCreateView(LoginRequiredMixin, View):
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
            song = form.save(commit=False)  # song = Song("nazwa", "rok", "ytLink")
            song.album_id = album.id  # song = Song("nazwa", "rok", "ytLink", "album")
            song.save()  # song.save to db
            return redirect('panel:albums:songs-index', album_id=album.id)
        return render(
            request,
            "contest/panel/song/create.html",
            {"form": form, "album": album}
        )


class SongEditView(LoginRequiredMixin, View):
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


class SongDeleteView(LoginRequiredMixin, View):
    def get(self, request, album_id, song_id):
        song = Song.objects.get(id=song_id)
        if song:
            song.delete()
        return redirect('panel:albums:songs-index', album_id=album_id)