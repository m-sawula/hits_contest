from django.core.management import BaseCommand

from contest.management.commands._private import recalculate_votes


class Command(BaseCommand):
    help = 'Calculate song view count'

    def handle(self, *args, **options):
        recalculate_votes()
        self.stdout.write(self.style.SUCCESS("Succesfully recalculte song votes"))

# mechanizm do przeliczania gloswów chodzący w tle, który pracuje z bazą danych
# nie obciąża serwera obsługującego stronę www

# funkcję uruchamia się poleceniem: python manage.py calculate_votes
