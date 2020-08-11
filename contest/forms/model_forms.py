from django import forms

from contest.models import Album, Song, SongVotes, ContestSubmission


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album  # z jakiego modelu korzystać ma klasa formularza
        fields = ['author', 'album_name']  # które pola będą wyświetlone w formularzu


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        # usuwamy z formularza "album" bo jest pobierany w widoku oraz sotr_order bo to będzie wypełniane automatycznie
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
