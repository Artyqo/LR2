from django.core.management.base import BaseCommand

from agency.models import Tour

COUNTRY_IMAGES = {
    'Испания': 'tours/spain.jpg',
    'Египет': 'tours/egypt.jpg',
    'Италия': 'tours/italy.jpg',
    'Турция': 'tours/turkey.jpg',
    'Греция': 'tours/greece.jpg',
}


class Command(BaseCommand):
    help = 'ЛР1: заполняет описание и картинку у путёвок (только пустые поля)'

    def handle(self, *args, **options):
        updated = 0
        for tour in Tour.objects.select_related('hotel', 'hotel__country'):
            changed = False
            if not tour.image and tour.hotel.country.name in COUNTRY_IMAGES:
                tour.image = COUNTRY_IMAGES[tour.hotel.country.name]
                changed = True
            if not tour.description:
                hotel = tour.hotel
                tour.description = (
                    f'{tour.title}. Вас ждёт отдых в стране «{hotel.country.name}» '
                    f'в отеле {hotel.name} ({hotel.stars}★). '
                    f'Длительность поездки — {tour.get_duration_weeks_display()}. '
                    f'В стоимость входит проживание, а наши менеджеры помогут '
                    f'с оформлением документов и трансфером.'
                )
                changed = True
            if changed:
                tour.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f'Обновлено путёвок: {updated}'))