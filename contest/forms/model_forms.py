from django import forms

from contest.models import Album, Song, SongVotes, ContestSubmission


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['author', 'album_name']


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        # usuwamy album bo jest pobierany w widoku oraz sotr order bo to będzie wypełniane automatycznie
        # fields = ['song_name', 'year', 'album', 'yt_link', 'sort_order']
        fields = ['song_name', 'year', 'yt_link']


class SongVotesForm(forms.ModelForm):
    class Meta:
        model = SongVotes
        fields = ['song', 'vote_hash']


class ContestSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContestSubmission
        fields = '__all__'
