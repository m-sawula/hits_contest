from contest.models import Song, SongVotes

def recalculate_votes():
    songs = Song.objects.all()
    for song in songs:
        song_votes_count = SongVotes.objects.filter(song_id=song.id).distinct('vote_hash').count()
        song.sort_order = song_votes_count
        song.save()

        # distinct('nazwa_zmiennej') podaje tylko unikale hasze
        # odfiltrowuje vote_hash tak, aby jenda osoba nie mogła głosować kilkakrotnie

        # rekalkulację głosów w tej aplikacji trzeba rocić ręcznie przez uruchamianie tej funkcji
