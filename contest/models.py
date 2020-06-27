from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    birth_date = models.DateField(null=True)
    band_name = models.CharField(max_length=255)
    debut = models.DateField(null=True)

    @property
    def name(self):
        if (self.first_name is not None) and (self.last_name is not None):
            return "{} {}".format(self.first_name, self.last_name)
        return self.band_name

    def __str__(self):
        return self.band_name


class Album(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")
    album_name = models.CharField(max_length=100)

    def __str__(self):
        return self.album_name


class Song(models.Model):
    song_name = models.CharField(max_length=64)
    year = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="album")
    yt_link = models.CharField(max_length=255, null=True)
    sort_order = models.IntegerField(default=0)

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
