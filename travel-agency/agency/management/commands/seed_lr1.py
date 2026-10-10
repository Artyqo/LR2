from django.core.management.base import BaseCommand

from agency.models import Banner, CompanyInfo, Employee, Partner

BANNERS = [
    # (файл в media/banners/, заголовок, ссылка, порядок)
    ('banner1.jpg', 'Горящие туры — скидки до 30%', '/tours/?is_hot=1', 1),
    ('banner2.jpg', 'Раннее бронирование на лето', '/tours/', 2),
    ('banner3.jpg', 'Отдых без хлопот — подберём путёвку', '/tours/', 3),
]

PARTNERS = [
    # (файл в media/partners/, название, сайт, порядок)
    ('belavia.png', 'Belavia', 'https://www.belavia.by/', 1),
    ('booking.png', 'Booking.com', 'https://www.booking.com/', 2),
    ('aviasales.png', 'Aviasales', 'https://www.aviasales.com/', 3),
    ('tripadvisor.png', 'Tripadvisor', 'https://www.tripadvisor.com/', 4),
    ('skyscanner.png', 'Skyscanner', 'https://www.skyscanner.net/', 5),
]

HISTORY = """2010 — открытие первого офиса в Минске и запуск первых автобусных туров.
2013 — заключены прямые договоры с турецкими и египетскими отелями.
2016 — открыт отдел индивидуальных путешествий.
2019 — запущен сайт с онлайн-подбором и бронированием путёвок.
2022 — более 10 000 довольных клиентов; расширение линейки направлений до 15 стран.
2025 — обновление сайта, корзина заказа и онлайн-оплата."""

REQUISITES = """Полное наименование: Общество с ограниченной ответственностью «Глобус Тревел»
УНП: 192837465
Юридический адрес: 220030, г. Минск, пр-т Независимости, 1
Расчётный счёт: BY20 OLMP 3135 0000 0010 0000 0933
Банк: ОАО «Банк Пример», BIC OLMPBY2X
Телефон: +375 (29) 111-22-33
E-mail: info@globustravel.by"""

CERTIFICATE = """СВИДЕТЕЛЬСТВО
о внесении сведений в Единый реестр туроператоров и турагентов
Регистрационный номер: 0001234
Дата внесения сведений: 14/03/2010
Общество с ограниченной ответственностью «Глобус Тревел»
УНП 192837465
Вид деятельности: турагентская деятельность
Свидетельство действительно при наличии действующего договора обязательного страхования.
Министр спорта и туризма ____________ / И. И. Петров /"""

EMPLOYEE_DESCRIPTION = {
    'Директор агентства': 'Руководит агентством, заключает договоры с туроператорами и отелями, принимает претензии и предложения клиентов.',
    'Ведущий менеджер по Европе': 'Подбирает и бронирует путёвки в страны Европы, рассчитывает стоимость, оформляет заказы и сопровождает клиента до вылета.',
    'Эксперт по экзотическим направлениям': 'Консультирует по дальним направлениям: Азия, Африка, острова. Составляет индивидуальные маршруты и экскурсионные программы.',
    'Визовый специалист': 'Готовит пакет документов для визы, записывает в визовые центры, проверяет страховки и сроки действия паспортов.',
}


class Command(BaseCommand):
    help = 'ЛР1: наполняет БД баннерами и партнёрами (можно запускать повторно)'

    def handle(self, *args, **options):
        for filename, title, link, order in BANNERS:
            obj, created = Banner.objects.update_or_create(
                title=title,
                defaults={'image': f'banners/{filename}',
                          'image_tablet': f"banners/{filename.replace('.jpg', '_tablet.jpg')}",
                          'image_mobile': f"banners/{filename.replace('.jpg', '_mobile.jpg')}",
                          'link_url': link, 'sort_order': order, 'is_active': True},
            )
            self.stdout.write(f"{'создан' if created else 'обновлён'} баннер: {obj.title}")

        for filename, name, site, order in PARTNERS:
            obj, created = Partner.objects.update_or_create(
                name=name,
                defaults={'logo': f'partners/{filename}', 'website': site,
                          'sort_order': order, 'is_active': True},
            )
            self.stdout.write(f"{'создан' if created else 'обновлён'} партнёр: {obj.name}")

        self._seed_company()
        self._seed_employees()
        self.stdout.write(self.style.SUCCESS('Готово.'))

    def _seed_company(self):
        info = CompanyInfo.objects.first() or CompanyInfo()
        info.logo = 'company/logo.png'
        info.video_file = 'company/promo.mp4'
        info.history_by_years = HISTORY
        info.requisites = REQUISITES
        info.certificate_text = CERTIFICATE
        info.save()
        self.stdout.write('обновлена информация о компании')

    def _seed_employees(self):
        for emp in Employee.objects.filter(description=''):
            emp.description = EMPLOYEE_DESCRIPTION.get(
                emp.position, 'Консультирует клиентов, подбирает путёвки и сопровождает заказ до вылета.')
            emp.save()