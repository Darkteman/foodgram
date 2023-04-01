import json

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    """
    Загрузка тегов из json файла в базу данных.
    """

    def handle(self, *args, **options):
        with open('data/tags.json', 'rb') as file:
            data = json.load(file)
            for item in data:
                tag, created = Tag.objects.get_or_create(
                    name=item['name'],
                    color=item['color'],
                    slug=item['slug']
                )
                if created:
                    print(f'Добавлен: {item["name"]}, '
                          f'{item["color"]}, {item["slug"]}')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
