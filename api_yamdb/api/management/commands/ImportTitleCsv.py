import csv

from django.core.management.base import BaseCommand

from api.models import Title


class Command(BaseCommand):
    help = 'Импорт данных из csv в таблицу Title'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category_id=row[3]
                )
