import hashlib  # importujemy całą bibliotekę

# porządki w importach 16:13

from django.shortcuts import render, redirect
from django.views import View
from contest.models import Author, Song, Album, SongVotes, ContestSubmission
from contest.forms.standard_forms import AuthorForm, LoginForm, VoteForm, ContestSubmissionForm
from contest.forms.model_forms import SongForm, AlbumForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# logowanie do panelu to specjalnie stworzony widok
# z pominięciem wbudowanego widoku logowania django
class LoginView(View):
    def get(self, request):
        # jeżeli user.id nie jest None przekieruj do panelu
        if request.user.id is not None:
            return redirect('panel:index')
        # w innym przypadku wyświetl formularz logowania
        return render(
            request,
            "contest/auth/login.html",
            # formlarz z pliku standard_forms.py
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
        # funkcja authenticate() sprawdza czy dane pobrane z forma znajdują się w bazie danych
        user = authenticate(
            request=request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )  # fetch user object

        if user is None:
            # jeżeli user jest None wyświetl komunikat
            messages.add_message(request, messages.WARNING, 'User does not exist in database!')
            # przekieruj na stronę logowania
            return redirect('login')
        # w innym przypadku utwórz sesje dla user
        login(request, user)  # session file and cookie
        # wyświetl wiadomość
        messages.add_message(request, messages.SUCCESS, 'User logged in successfully')
        # przekieruj na stronę
        return redirect('panel:index')


@login_required
def logout_view(request):
    logout(request)
    return redirect('common-index')


# główna strona palikacji dla nie zalogowanych, url: http://127.0.0.1:8000
class CommonIndexView(View):
    def get(self, request):
        # nie trzeba zapisywać danych z forms do zmiennych można je podać bezpośrednio do kontekstu
        # songs = Song.objects.all().order_by('sort_order'),
        # vote_form = VoteForm()
        # contest_from = ContestSubmissionForm()
        return render(
            request,
            "contest/common/index.html",
            {
                # do szablonu html przekazywane są posortowane piosenki
                "songs": Song.objects.all().order_by('sort_order'),
                "vote_form": VoteForm(),
                "contest_form": ContestSubmissionForm()
            }
        )


class VoteView(View):
    # dziełanie VoteView
    # odbieranie z VoteForm
    # znajdowanie przesłanego id songa w bazie danych
    # jeślie nie ma id soga to redirect 'common-index' z message error "nie ma tekiej piosenki"
    # vote_hash zawiera funkcję hashująca oddany głoś na piosenkę,
    # aby zablokować możliwość wielokrotnego głosowania przez jedną osobę
    # zapisuje całość jako SongVotes.create()
    # redirect 'common-index' z massage succes "dziekujemy za głos"
    def post(self, request):
        vote_form = VoteForm(request.POST)
        if not vote_form.is_valid():
            messages.add_message(
                request,
                messages.WARNING,
                "Coś poszło nie tak."
            )
            return redirect('common-index')

        song = Song.objects.get(id=vote_form.cleaned_data['song_data'])
        if not song:
            messages.add_message(
                request,
                messages.WARNING,
                "Nie ma takiej piosenki."
            )
            return redirect('common-index')
        SongVotes.objects.create(
            song=song,
            vote_hash=hashlib.md5(
                request.headers.get('User-Agent').encode()
            ).hexdigest()
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            "Dziękujemy za udział w konkursie."
        )
        return redirect('common-index')


class ContestSubmissionView(View):
    # działanie ContestSubmissionView
    # odbiera dane z ContestSubissionForm
    # szuka id songa w bazie danch
    # jeślie nie ma id soga to redirect 'common-index' z message error "nie ma tekiej piosenk
    # zapisuje dane osoby głosującej do bazy
    # przekierowuje na common-index i wyświetla komunikat sukcesu
    def post(self, request):
        form = ContestSubmissionForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, 'Coś poszło nie tak')
            return redirect('common-index')

        song = Song.objects.get(id=form.cleaned_data['song_data'])
        if not song:
            messages.add_message(request, messages.WARNING, 'Nie ma takiej piosenki')
            return redirect('common-index')
        ContestSubmission.objects.create(
            song=song,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            telephone=form.cleaned_data['telephone'],
            email=form.cleaned_data['email'],
            context=form.cleaned_data['context']
        )
        messages.add_message(request, messages.SUCCESS, 'Dziękujemy za udział w konkursie')
        return redirect('common-index')


# główna strona dla ZALOGOWANYCH, url: http://127.0.0.1:8000/panel/
class PanelIndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "contest/panel/index.html")


# author CRUD (create, read, update and delete)
# obsłużony jest przez standard views i standard forms


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
        birth_date = None
        debut = None
        if author.birth_date is not None:
            birth_date = author.birth_date.strftime('%d/%m/%Y')

        if author.debut is not None:
            debut = author.debut.strftime('%d/%m/%Y')

        form = AuthorForm({
            "fist_name": author.first_name,
            "last_name": author.last_name,
            "birth_date": birth_date,
            "band_name": author.band_name,
            "debut": debut
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


# song CRUD (create, read, update and delete)
# obsłużony jest przez generic views i model forms


class SongIndexView(LoginRequiredMixin, View):
    def get(self, request, album_id):
        # rozwiązanie najmniej obciążające aplikację
        # pobrać model i model nadrzędny w tym przypadku piosenkę i album
        album = Album.objects.get(id=album_id)
        songs = Song.objects.filter(album_id=album_id)
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

    # klasyczne zapisanie piosenki wyglądałoby tak:

    # def post(self, request, album_id):
    #     form = SongForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('panel:albums:songs-index', album_id=album_id)

    # w tej aplikacji jest potrzeba, aby nie można było dodać piosenki
    # bez uprzedniego wybrania albumu
    def post(self, request, album_id):
        form = SongForm(request.POST)
        album = Album.objects.get(id=album_id)

        if form.is_valid():
            # commit=False wyłącza zapisywanie danych pobranych przez formularz
            # commit=False wyłącza zapisywanie danych pobranych przez formularz
            #           # obiekt czeka w pamięci do czasu zaktualizowania danych
            #           # powstaje obiek (piosenka) bez jego zapisnia dodbazy
            song = form.save(commit=False)  # song = Song("nazwa", "rok", "ytLink")
            # do piosenki zawieszonej w pamięci dodajemy album
            song.album_id = album.id  # song = Song("nazwa", "rok", "ytLink", "album")
            # i doiero teraz zapisujemy całość do bazy danych
            song.save()  # song.save to db
            return redirect('panel:albums:songs-index', album_id=album.id)
        return render(
            request,
            "contest/panel/song/create.html",
            {"form": form, "album": album}
        )


class SongUpdateView(LoginRequiredMixin, View):
    def get(self, request, album_id, song_id):
        album = Album.objects.get(pk=album_id)
        song = Song.objects.get(pk=song_id)
        # instance (działa z ModelForm) wstawia do wyświetlanego formularza
        # dane pobranej pioseki, którą bedziemy aktualizować
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
