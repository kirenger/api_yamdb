import csv

from django.core.management.base import BaseCommand

from api.models import Genre


class Command(BaseCommand):
    help = 'Импорт данных из csv в таблицу Genre'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                Genre.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )
