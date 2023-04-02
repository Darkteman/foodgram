import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """
    Загрузка ингредиентов из json файла в базу данных.
    """

    def handle(self, *args, **options):
        with open('data/ingredients.json', 'rb') as file:
            data = json.load(file)
            for item in data:
                ingredient, created = Ingredient.objects.get_or_create(
                    name=item['name'].title(),
                    measurement_unit=item['measurement_unit']
                )
                if created:
                    print(f'Добавлен: {item["name"]}, '
                          f'{item["measurement_unit"]}')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
