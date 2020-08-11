from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime


class Author(models.Model):
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    birth_date = models.DateField(null=True)
    band_name = models.CharField(max_length=255)
    debut = models.DateField(null=True, verbose_name="rok debiutu")

    @property
    def name(self):
        if (self.first_name is not None) and (self.last_name is not None):
            return "{} {}".format(self.first_name, self.last_name)
        return self.band_name

    def __str__(self):
        return self.band_name

class Album(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Nazwa zespołu", related_name="author")
    album_name = models.CharField(max_length=100, verbose_name="Nazwa albumu")
    # poniżej ustawiamy jakie informacje będzie zwracać klasa
    # ponieważ "author" ma klucz obcy do Author to "Album" może zwracać dane z klasy Author
    def __str__(self):
        return f"{self.album_name} ({self.author.band_name})"


class Song(models.Model):
    song_name = models.CharField(max_length=64)
    year = models.IntegerField(verbose_name="Rok powstania piosenki")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="album")
    yt_link = models.CharField(max_length=255, null=True, )
    sort_order = models.IntegerField(default=0)

    # walidator dla pola "year" i "yt_link"
    def clean(self):
        if int(self.year) < 1900 or int(self.year) > datetime.now().year:
            raise ValidationError('Year is not valid, it should be between 1900 - curren year')
        if self.yt_link != '#' and not self.yt_link.startswith('https://www.youtube.com'):
            raise ValidationError('Wrong youtube link!')

    def __str__(self):
        return "{} ({})".format(self.song_name, self.album.album_name)


class SongVotes(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="songVotes")
    vote_hash = models.TextField()

    def __str__(self):
        return self.vote_hash


class ContestSubmission(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="songSubmission")
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    telephone = models.CharField(max_length=15)
    email = models.CharField(max_length=64)
    context = models.TextField()

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.song.song_name)
