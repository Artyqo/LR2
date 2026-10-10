from django.test import TestCase, Client as TestClient
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime

from .models import (
    Country, Hotel, Tour, Employee, Client,
    Order, Review, PromoCode, FAQ, Vacancy, News, CompanyInfo
)
from .models import phone_validator, validate_adult


class PhoneValidatorTest(TestCase):
    def test_valid_phone_29(self):
        try:
            phone_validator('+375 (29) 123-45-67')
        except ValidationError:
            self.fail('Валидный номер не прошёл валидацию')

    def test_valid_phone_33(self):
        try:
            phone_validator('+375 (33) 123-45-67')
        except ValidationError:
            self.fail('Валидный номер не прошёл валидацию')

    def test_invalid_phone_no_plus(self):
        with self.assertRaises(ValidationError):
            phone_validator('375 (29) 123-45-67')

    def test_invalid_phone_wrong_code(self):
        with self.assertRaises(ValidationError):
            phone_validator('+375 (28) 123-45-67')

    def test_invalid_phone_format(self):
        with self.assertRaises(ValidationError):
            phone_validator('+375 29 1234567')


class AgeValidatorTest(TestCase):
    def test_adult_passes(self):
        birth = datetime.date.today().replace(year=datetime.date.today().year - 20)
        try:
            validate_adult(birth)
        except ValidationError:
            self.fail('Совершеннолетний не прошёл валидацию')

    def test_minor_fails(self):
        birth = datetime.date.today().replace(year=datetime.date.today().year - 17)
        with self.assertRaises(ValidationError):
            validate_adult(birth)

    def test_exactly_18_passes(self):
        today = datetime.date.today()
        birth = today.replace(year=today.year - 18)
        try:
            validate_adult(birth)
        except ValidationError:
            self.fail('Ровно 18 лет не прошло валидацию')


class TourPriceTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            name='Тестовая страна',
            climate_winter='холодно',
            climate_spring='тепло',
            climate_summer='жарко',
            climate_autumn='прохладно',
        )
        self.hotel = Hotel.objects.create(
            country=self.country,
            name='Тестовый отель',
            stars=3,
            price_per_day=100.00,
        )

    def test_price_one_week(self):
        tour = Tour(hotel=self.hotel, title='Тест', duration_weeks=1,
                    departure_date=datetime.date.today())
        self.assertEqual(tour.price, 700)

    def test_price_two_weeks(self):
        tour = Tour(hotel=self.hotel, title='Тест', duration_weeks=2,
                    departure_date=datetime.date.today())
        self.assertEqual(tour.price, 1400)

    def test_price_four_weeks(self):
        tour = Tour(hotel=self.hotel, title='Тест', duration_weeks=4,
                    departure_date=datetime.date.today())
        self.assertEqual(tour.price, 2800)


class CountryHotelRelationTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            name='Испания',
            climate_winter='мягкий',
            climate_spring='тёплый',
            climate_summer='жаркий',
            climate_autumn='бархатный',
        )
        Hotel.objects.create(country=self.country, name='Отель 1', stars=4, price_per_day=120)
        Hotel.objects.create(country=self.country, name='Отель 2', stars=5, price_per_day=200)

    def test_country_has_hotels(self):
        self.assertEqual(self.country.hotels.count(), 2)

    def test_hotel_str(self):
        hotel = Hotel.objects.get(name='Отель 1')
        self.assertIn('Отель 1', str(hotel))


class PromoCodeTest(TestCase):
    def setUp(self):
        PromoCode.objects.create(code='ACTIVE10', discount_amount=10, is_active=True)
        PromoCode.objects.create(code='OLD20', discount_amount=20, is_active=False)

    def test_active_promo(self):
        self.assertEqual(PromoCode.objects.filter(is_active=True).count(), 1)

    def test_archive_promo(self):
        self.assertEqual(PromoCode.objects.filter(is_active=False).count(), 1)

    def test_promo_str(self):
        promo = PromoCode.objects.get(code='ACTIVE10')
        self.assertIn('ACTIVE10', str(promo))
        self.assertIn('Активен', str(promo))

class ViewsPublicTest(TestCase):
    """Тесты публичных страниц — доступны всем без авторизации"""

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_news_page(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)

    def test_faq_page(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_vacancies_page(self):
        response = self.client.get(reverse('vacancies'))
        self.assertEqual(response.status_code, 200)

    def test_promocodes_page(self):
        response = self.client.get(reverse('promocodes'))
        self.assertEqual(response.status_code, 200)

    def test_reviews_page(self):
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_page(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)

    def test_tour_list_page(self):
        response = self.client.get(reverse('tour_list'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)


class ViewsAuthTest(TestCase):
    """Тесты доступа к защищённым страницам"""

    def setUp(self):
        # Обычный пользователь без роли
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )
        # Суперпользователь
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
        )

    def test_profile_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/login/?next=/profile/')

    def test_statistics_forbidden_for_guest(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 403)

    def test_statistics_forbidden_for_regular_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 403)

    def test_statistics_accessible_for_admin(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)

    def test_tour_create_forbidden_for_guest(self):
        response = self.client.get(reverse('tour_create'))
        self.assertEqual(response.status_code, 403)

    def test_tour_create_accessible_for_admin(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('tour_create'))
        self.assertEqual(response.status_code, 200)

    def test_login_works(self):
        self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        # Проверяем что пользователь залогинен
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_works(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, '/')


class RegistrationTest(TestCase):
    """Тесты регистрации клиента"""

    def test_valid_registration(self):
        response = self.client.post(reverse('register'), {
            'username':   'newclient',
            'last_name':  'Тестов',
            'first_name': 'Тест',
            'address':    'г. Минск, ул. Тестовая, 1',
            'phone':      '+375 (29) 999-88-77',
            'birth_date': '1990-01-01',
            'timezone':   'Europe/Minsk',
            'password1':  'StrongPass123!',
            'password2':  'StrongPass123!',
        })
        self.assertTrue(User.objects.filter(username='newclient').exists())
        self.assertTrue(Client.objects.filter(user__username='newclient').exists())

    def test_invalid_phone_rejected(self):
        response = self.client.post(reverse('register'), {
            'username':   'newclient2',
            'last_name':  'Тестов',
            'first_name': 'Тест',
            'address':    'г. Минск, ул. Тестовая, 1',
            'phone':      '89991234567',
            'birth_date': '1990-01-01',
            'timezone':   'Europe/Minsk',
            'password1':  'StrongPass123!',
            'password2':  'StrongPass123!',
        })
        self.assertFalse(User.objects.filter(username='newclient2').exists())

    def test_minor_rejected(self):
        response = self.client.post(reverse('register'), {
            'username':   'newclient3',
            'last_name':  'Тестов',
            'first_name': 'Тест',
            'address':    'г. Минск, ул. Тестовая, 1',
            'phone':      '+375 (29) 999-88-77',
            'birth_date': '2015-01-01',
            'timezone':   'Europe/Minsk',
            'password1':  'StrongPass123!',
            'password2':  'StrongPass123!',
        })
        self.assertFalse(User.objects.filter(username='newclient3').exists())

class TourViewsTest(TestCase):
    """Тесты каталога туров — фильтрация, поиск, детали"""

    def setUp(self):
        self.country = Country.objects.create(
            name='Тест страна',
            climate_winter='холодно',
            climate_spring='тепло',
            climate_summer='жарко',
            climate_autumn='прохладно',
        )
        self.hotel = Hotel.objects.create(
            country=self.country,
            name='Тест отель',
            stars=4,
            price_per_day=100.00,
        )
        self.tour = Tour.objects.create(
            hotel=self.hotel,
            title='Тестовый тур',
            duration_weeks=1,
            departure_date=datetime.date.today() + datetime.timedelta(days=10),
            is_hot=False,
        )

    def test_tour_list_returns_tours(self):
        response = self.client.get(reverse('tour_list'))
        self.assertContains(response, 'Тестовый тур')

    def test_tour_detail(self):
        response = self.client.get(reverse('tour_detail', args=[self.tour.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый тур')

    def test_tour_filter_by_country(self):
        response = self.client.get(reverse('tour_list'), {'country': self.country.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый тур')

    def test_tour_filter_by_stars(self):
        response = self.client.get(reverse('tour_list'), {'stars': 4})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый тур')

    def test_tour_filter_hot(self):
        response = self.client.get(reverse('tour_list'), {'is_hot': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Тестовый тур')

    def test_tour_search(self):
        response = self.client.get(reverse('tour_list'), {'q': 'Тестовый'})
        self.assertContains(response, 'Тестовый тур')

    def test_tour_search_no_results(self):
        response = self.client.get(reverse('tour_list'), {'q': 'несуществующий'})
        self.assertNotContains(response, 'Тестовый тур')

    def test_tour_sort_price_asc(self):
        response = self.client.get(reverse('tour_list'), {'sort': 'price_asc'})
        self.assertEqual(response.status_code, 200)

    def test_tour_delete_by_admin(self):
        admin = User.objects.create_superuser(
            username='admin2', password='adminpass123'
        )
        self.client.login(username='admin2', password='adminpass123')
        response = self.client.post(reverse('tour_delete', args=[self.tour.pk]))
        self.assertRedirects(response, reverse('tour_list'))
        self.assertFalse(Tour.objects.filter(pk=self.tour.pk).exists())

    def test_tour_delete_forbidden_for_guest(self):
        response = self.client.post(reverse('tour_delete', args=[self.tour.pk]))
        self.assertEqual(response.status_code, 403)


class ProfileViewTest(TestCase):
    """Тесты личного кабинета для разных ролей"""

    def setUp(self):
        self.country = Country.objects.create(
            name='Профиль страна',
            climate_winter='х', climate_spring='т',
            climate_summer='ж', climate_autumn='п',
        )
        self.hotel = Hotel.objects.create(
            country=self.country, name='Профиль отель',
            stars=3, price_per_day=50.00,
        )
        # Клиент
        self.client_user = User.objects.create_user(
            username='client_user', password='pass123'
        )
        self.client_profile = Client.objects.create(
            user=self.client_user,
            last_name='Тестов', first_name='Клиент',
            address='г. Минск', phone='+375 (29) 111-11-11',
            birth_date=datetime.date(1990, 1, 1),
            timezone='Europe/Minsk',
        )
        # Сотрудник
        self.emp_user = User.objects.create_user(
            username='emp_user', password='pass123'
        )
        self.employee = Employee.objects.create(
            user=self.emp_user,
            full_name='Тестов Сотрудник',
            position='Менеджер',
            phone='+375 (29) 222-22-22',
            birth_date=datetime.date(1985, 5, 10),
            email='emp@test.by',
        )
        # Админ
        self.admin_user = User.objects.create_superuser(
            username='admin3', password='adminpass123'
        )

    def test_client_profile_accessible(self):
        self.client.login(username='client_user', password='pass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Клиент')

    def test_employee_profile_accessible(self):
        self.client.login(username='emp_user', password='pass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестов Сотрудник')

    def test_admin_profile_accessible(self):
        self.client.login(username='admin3', password='adminpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_user_without_role_redirected(self):
        bare_user = User.objects.create_user(
            username='bare_user', password='pass123'
        )
        self.client.login(username='bare_user', password='pass123')
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, reverse('index'))


class ReviewsTest(TestCase):
    """Тесты отзывов"""

    def setUp(self):
        self.client_user = User.objects.create_user(
            username='reviewer', password='pass123'
        )
        self.client_profile = Client.objects.create(
            user=self.client_user,
            last_name='Отзывов', first_name='Тест',
            address='г. Минск', phone='+375 (29) 333-33-33',
            birth_date=datetime.date(1990, 1, 1),
            timezone='Europe/Minsk',
        )

    def test_guest_cannot_post_review(self):
        response = self.client.post(reverse('reviews'), {
            'author_name': 'Гость',
            'text': 'Отличный отдых!',
            'rating': 5,
        })
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Review.objects.count(), 0)

    def test_client_can_post_review(self):
        self.client.login(username='reviewer', password='pass123')
        response = self.client.post(reverse('reviews'), {
            'author_name': 'reviewer',
            'text': 'Отличный отдых был!',
            'rating': 5,
        })
        self.assertRedirects(response, reverse('reviews'))
        self.assertEqual(Review.objects.count(), 1)

    def test_review_saved_correctly(self):
        self.client.login(username='reviewer', password='pass123')
        self.client.post(reverse('reviews'), {
            'author_name': 'reviewer',
            'text': 'Прекрасное путешествие!',
            'rating': 4,
        })
        review = Review.objects.first()
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.text, 'Прекрасное путешествие!')

# =========================================================================
# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ (повышение покрытия до 80%+)
# =========================================================================
from unittest.mock import patch, MagicMock

import requests
from django.test import override_settings
from django.utils import timezone as dj_timezone
from django.contrib.auth.models import AnonymousUser

from . import views
from .templatetags.dt_extras import format_dual, get_user_tz_name


def make_country(name='Тест-страна'):
    return Country.objects.create(
        name=name, climate_winter='х', climate_spring='т',
        climate_summer='ж', climate_autumn='п',
    )


def make_hotel(country=None, stars=4, price=100):
    country = country or make_country()
    return Hotel.objects.create(
        country=country, name=f'Отель {country.name}', stars=stars, price_per_day=price,
    )


def make_tour(hotel=None, title='Тур', weeks=1, hot=False):
    hotel = hotel or make_hotel()
    return Tour.objects.create(
        hotel=hotel, title=title, duration_weeks=weeks,
        departure_date=datetime.date.today() + datetime.timedelta(days=30), is_hot=hot,
    )


def make_client_user(username='cl', tz='Europe/Minsk', birth=datetime.date(1990, 1, 1)):
    user = User.objects.create_user(username=username, password='pass12345')
    profile = Client.objects.create(
        user=user, last_name=f'Фамилия{username}', first_name='Имя',
        address='г. Минск', phone='+375 (29) 111-11-11',
        birth_date=birth, timezone=tz,
    )
    return user, profile


def make_employee_user(username='em', tz='Europe/Minsk'):
    user = User.objects.create_user(username=username, password='pass12345')
    profile = Employee.objects.create(
        user=user, full_name=f'Сотрудник {username}', position='Менеджер',
        phone='+375 (29) 222-22-22', birth_date=datetime.date(1985, 5, 10),
        email=f'{username}@test.by', timezone=tz,
    )
    return user, profile


def make_order(client_profile, employee_profile, tour):
    order = Order.objects.create(
        client=client_profile, employee=employee_profile, total_cost=tour.price,
    )
    order.tours.add(tour)
    return order


def fake_response(status=200, payload=None):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = payload
    return resp


# ---------------------------- внешние API ----------------------------

class WeatherApiTest(TestCase):
    PAYLOAD = {
        'name': 'Madrid',
        'main': {'temp': 20.4, 'feels_like': 19.6, 'humidity': 55},
        'weather': [{'description': 'ясно', 'icon': '01d'}],
        'wind': {'speed': 3.2},
    }

    @override_settings(OPENWEATHER_API_KEY='')
    def test_no_api_key_returns_none(self):
        self.assertIsNone(views.get_weather_for_country('Испания'))

    @override_settings(OPENWEATHER_API_KEY='key')
    def test_unknown_country_returns_none(self):
        self.assertIsNone(views.get_weather_for_country('Атлантида'))

    @override_settings(OPENWEATHER_API_KEY='key')
    @patch('agency.views.requests.get')
    def test_success(self, mock_get):
        mock_get.return_value = fake_response(200, self.PAYLOAD)
        result = views.get_weather_for_country('Испания')
        self.assertEqual(result['temp'], 20)
        self.assertEqual(result['feels_like'], 20)
        self.assertEqual(result['city_ru'], 'Мадрид')
        self.assertEqual(result['description'], 'Ясно')

    @override_settings(OPENWEATHER_API_KEY='key')
    @patch('agency.views.requests.get')
    def test_bad_status_returns_none(self, mock_get):
        mock_get.return_value = fake_response(401, {})
        self.assertIsNone(views.get_weather_for_country('Испания'))

    @override_settings(OPENWEATHER_API_KEY='key')
    @patch('agency.views.requests.get', side_effect=requests.RequestException('boom'))
    def test_request_exception_returns_none(self, mock_get):
        self.assertIsNone(views.get_weather_for_country('Испания'))


class NbrbApiTest(TestCase):
    RATES = [
        {'Cur_Abbreviation': 'USD', 'Cur_OfficialRate': 3.0, 'Cur_Scale': 1},
        {'Cur_Abbreviation': 'EUR', 'Cur_OfficialRate': 3.5, 'Cur_Scale': 1},
        {'Cur_Abbreviation': 'RUB', 'Cur_OfficialRate': 3.5, 'Cur_Scale': 100},
        {'Cur_Abbreviation': 'PLN', 'Cur_OfficialRate': 0.8, 'Cur_Scale': 1},
    ]

    @patch('agency.views.requests.get')
    def test_success(self, mock_get):
        mock_get.return_value = fake_response(200, self.RATES)
        rates = views.get_nbrb_rates()
        self.assertEqual(rates['USD'], 3.0)
        self.assertEqual(rates['EUR'], 3.5)
        self.assertAlmostEqual(rates['RUB'], 0.035)
        self.assertNotIn('PLN', rates)

    @patch('agency.views.requests.get')
    def test_no_needed_currencies_returns_none(self, mock_get):
        mock_get.return_value = fake_response(200, [self.RATES[3]])
        self.assertIsNone(views.get_nbrb_rates())

    @patch('agency.views.requests.get')
    def test_bad_status_returns_none(self, mock_get):
        mock_get.return_value = fake_response(500, [])
        self.assertIsNone(views.get_nbrb_rates())

    @patch('agency.views.requests.get', side_effect=requests.RequestException('boom'))
    def test_request_exception_returns_none(self, mock_get):
        self.assertIsNone(views.get_nbrb_rates())


class TourDetailApiTest(TestCase):
    def setUp(self):
        self.tour = make_tour()  # 1 неделя * 100 = 700

    @patch('agency.views.get_nbrb_rates', return_value={'USD': 3.0, 'EUR': 3.5, 'RUB': 0.035})
    @patch('agency.views.get_weather_for_country', return_value={
        'temp': 20, 'feels_like': 19, 'humidity': 50, 'description': 'Ясно',
        'icon': '01d', 'wind_speed': 3, 'city_ru': 'Мадрид'})
    def test_detail_with_weather_and_rates(self, _weather, _rates):
        response = self.client.get(reverse('tour_detail', args=[self.tour.pk]))
        self.assertEqual(response.status_code, 200)
        prices = response.context['currency_prices']
        self.assertEqual(prices['USD'], round(700 / 3.0, 2))
        self.assertEqual(prices['EUR'], round(700 / 3.5, 2))
        self.assertContains(response, 'Мадрид')

    @patch('agency.views.get_nbrb_rates', return_value=None)
    @patch('agency.views.get_weather_for_country', return_value=None)
    def test_detail_when_apis_unavailable(self, _weather, _rates):
        response = self.client.get(reverse('tour_detail', args=[self.tour.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['currency_prices'])

    def test_detail_404(self):
        with patch('agency.views.get_nbrb_rates', return_value=None), \
                patch('agency.views.get_weather_for_country', return_value=None):
            response = self.client.get(reverse('tour_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    @patch('agency.views.get_nbrb_rates', return_value=None)
    @patch('agency.views.get_weather_for_country', return_value=None)
    def test_client_sees_employees_list(self, _w, _r):
        user, _ = make_client_user('detail_cl')
        make_employee_user('detail_em')
        self.client.login(username='detail_cl', password='pass12345')
        response = self.client.get(reverse('tour_detail', args=[self.tour.pk]))
        self.assertTrue(response.context['can_buy'])
        self.assertEqual(response.context['employees'].count(), 1)


# ---------------------------- покупка тура ----------------------------

class TourBuyTest(TestCase):
    def setUp(self):
        self.tour = make_tour()
        self.cl_user, self.cl = make_client_user('buyer')
        self.em_user, self.em = make_employee_user('seller')
        self.url = reverse('tour_buy', args=[self.tour.pk])

    def test_guest_redirected_to_login(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_admin_cannot_buy(self):
        User.objects.create_superuser('boss', password='adminpass123')
        self.client.login(username='boss', password='adminpass123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tour_detail', args=[self.tour.pk]),
                             fetch_redirect_response=False)
        self.assertEqual(Order.objects.count(), 0)

    def test_client_buys_with_chosen_employee(self):
        self.client.login(username='buyer', password='pass12345')
        response = self.client.post(self.url, {'employee_id': self.em.pk})
        self.assertRedirects(response, reverse('profile'), fetch_redirect_response=False)
        order = Order.objects.get()
        self.assertEqual(order.employee, self.em)
        self.assertEqual(order.total_cost, self.tour.price)
        self.assertIn(self.tour, order.tours.all())

    def test_client_buys_with_invalid_employee_falls_back(self):
        self.client.login(username='buyer', password='pass12345')
        self.client.post(self.url, {'employee_id': 99999})
        self.assertEqual(Order.objects.get().employee, self.em)

    def test_client_reuses_previous_manager(self):
        _, other_em = make_employee_user('seller2')
        make_order(self.cl, other_em, self.tour)
        self.client.login(username='buyer', password='pass12345')
        self.client.post(self.url)
        self.assertEqual(Order.objects.filter(client=self.cl).count(), 2)

    def test_no_employees_available(self):
        self.em_user.delete()  # каскадно удалит и Employee
        self.client.login(username='buyer', password='pass12345')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tour_detail', args=[self.tour.pk]),
                             fetch_redirect_response=False)
        self.assertEqual(Order.objects.count(), 0)


# ---------------------------- CRUD туров ----------------------------

class TourCrudTest(TestCase):
    def setUp(self):
        self.hotel = make_hotel()
        self.tour = make_tour(self.hotel, title='Старое имя')
        User.objects.create_superuser('crud_admin', password='adminpass123')
        self.client.login(username='crud_admin', password='adminpass123')

    def valid_data(self, title='Новый тур'):
        return {
            'hotel': self.hotel.pk, 'title': title, 'duration_weeks': 2,
            'departure_date': '2026-12-01',
        }

    def test_create_get(self):
        self.assertEqual(self.client.get(reverse('tour_create')).status_code, 200)

    def test_create_valid(self):
        response = self.client.post(reverse('tour_create'), self.valid_data())
        self.assertRedirects(response, reverse('tour_list'))
        self.assertTrue(Tour.objects.filter(title='Новый тур').exists())

    def test_create_invalid(self):
        data = self.valid_data()
        data['title'] = ''
        response = self.client.post(reverse('tour_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tour.objects.count(), 1)

    def test_update_get(self):
        response = self.client.get(reverse('tour_update', args=[self.tour.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_valid(self):
        response = self.client.post(reverse('tour_update', args=[self.tour.pk]),
                                    self.valid_data('Обновлённый'))
        self.assertRedirects(response, reverse('tour_detail', args=[self.tour.pk]),
                             fetch_redirect_response=False)
        self.tour.refresh_from_db()
        self.assertEqual(self.tour.title, 'Обновлённый')

    def test_update_invalid(self):
        data = self.valid_data()
        data['departure_date'] = 'не дата'
        response = self.client.post(reverse('tour_update', args=[self.tour.pk]), data)
        self.assertEqual(response.status_code, 200)

    def test_delete_confirm_page(self):
        response = self.client.get(reverse('tour_delete', args=[self.tour.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Tour.objects.filter(pk=self.tour.pk).exists())

    def test_regular_user_cannot_update(self):
        self.client.logout()
        make_client_user('plain')
        self.client.login(username='plain', password='pass12345')
        response = self.client.post(reverse('tour_update', args=[self.tour.pk]),
                                    self.valid_data())
        self.assertEqual(response.status_code, 403)


class TourListFiltersTest(TestCase):
    def setUp(self):
        self.tour = make_tour(title='Дешёвый', hot=True)  # 700

    def test_price_filter_excludes(self):
        response = self.client.get(reverse('tour_list'), {'price': '100'})
        self.assertNotContains(response, 'Дешёвый')

    def test_price_filter_includes(self):
        response = self.client.get(reverse('tour_list'), {'price': '10000'})
        self.assertContains(response, 'Дешёвый')

    def test_all_sort_modes(self):
        for mode in ('departure', 'price_asc', 'price_desc', 'country', 'stars_desc', 'bad'):
            response = self.client.get(reverse('tour_list'), {'sort': mode})
            self.assertEqual(response.status_code, 200, mode)

    def test_bad_numeric_filters_ignored(self):
        response = self.client.get(reverse('tour_list'), {'country': 'abc', 'stars': 'x'})
        self.assertEqual(response.status_code, 200)

    def test_date_format_slash(self):
        response = self.client.get(reverse('tour_list'))
        expected = self.tour.departure_date.strftime('%d/%m/%Y')
        self.assertContains(response, expected)


# ---------------------------- профиль с заказами ----------------------------

class ProfileWithOrdersTest(TestCase):
    def setUp(self):
        self.tour = make_tour()
        self.cl_user, self.cl = make_client_user('pc', tz='Asia/Tokyo')
        self.em_user, self.em = make_employee_user('pe', tz='Europe/London')
        make_order(self.cl, self.em, self.tour)

    def test_client_sees_orders_and_dates(self):
        self.client.login(username='pc', password='pass12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
        self.assertEqual(response.context['user_tz_name'], 'Asia/Tokyo')
        self.assertIn('/', response.context['local_now_str'])
        self.assertContains(response, self.tour.departure_date.strftime('%d/%m/%Y'))

    def test_employee_sees_orders_and_clients(self):
        self.client.login(username='pe', password='pass12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
        self.assertEqual(response.context['my_clients'].count(), 1)
        self.assertEqual(response.context['user_tz_name'], 'Europe/London')

    def test_admin_sees_clients_and_hotels(self):
        User.objects.create_superuser('pa', password='adminpass123')
        self.client.login(username='pa', password='adminpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['clients'].count(), 1)
        self.assertContains(response, self.tour.departure_date.strftime('%d/%m/%Y'))


# ---------------------------- статистика и графики ----------------------------

class StatisticsTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('stat_admin', password='adminpass123')
        self.client.login(username='stat_admin', password='adminpass123')

    def test_statistics_empty(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sales_stats'], {})
        self.assertEqual(response.context['age_stats'], {})

    def test_statistics_with_data(self):
        em_user, em = make_employee_user('stat_em')
        cheap = make_tour(make_hotel(make_country('А-страна'), stars=3, price=50), title='t1')
        rich = make_tour(make_hotel(make_country('Б-страна'), stars=5, price=200), title='t2')
        _, c1 = make_client_user('c1', birth=datetime.date(1990, 1, 1))
        _, c2 = make_client_user('c2', birth=datetime.date(2000, 6, 15))
        _, c3 = make_client_user('c3', birth=datetime.date(1980, 3, 3))
        make_order(c1, em, cheap)
        make_order(c2, em, cheap)
        make_order(c3, em, rich)

        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)

        sales = response.context['sales_stats']
        self.assertEqual(sales['count'], 3)
        self.assertEqual(sales['total'], round(350 * 2 + 1400, 2))
        self.assertEqual(sales['mode'], 350.0)
        self.assertEqual(sales['median'], 350.0)

        ages = response.context['age_stats']
        self.assertEqual(ages['count'], 3)
        self.assertGreaterEqual(ages['max'], ages['min'])

        self.assertEqual(response.context['most_popular'].name, 'А-страна')
        self.assertEqual(response.context['most_profitable'].name, 'Б-страна')
        names = [c.last_name for c in response.context['clients_alpha']]
        self.assertEqual(names, sorted(names))


class ChartsTest(TestCase):
    CHART_URLS = ('chart_sales_by_country', 'chart_tours_by_stars', 'chart_orders_by_month')

    def test_guest_forbidden(self):
        for name in self.CHART_URLS:
            self.assertEqual(self.client.get(reverse(name)).status_code, 403, name)

    def test_regular_user_forbidden(self):
        make_client_user('chart_cl')
        self.client.login(username='chart_cl', password='pass12345')
        for name in self.CHART_URLS:
            self.assertEqual(self.client.get(reverse(name)).status_code, 403, name)

    def test_orders_by_month_without_data(self):
        User.objects.create_superuser('chart_admin0', password='adminpass123')
        self.client.login(username='chart_admin0', password='adminpass123')
        response = self.client.get(reverse('chart_orders_by_month'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_all_charts_with_data(self):
        _, em = make_employee_user('chart_em')
        _, cl = make_client_user('chart_cl2')
        make_order(cl, em, make_tour(make_hotel(make_country('Ч1'), stars=3)))
        make_order(cl, em, make_tour(make_hotel(make_country('Ч2'), stars=5)))
        User.objects.create_superuser('chart_admin', password='adminpass123')
        self.client.login(username='chart_admin', password='adminpass123')
        for name in self.CHART_URLS:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)
            self.assertEqual(response['Content-Type'], 'image/png', name)
            self.assertTrue(response.content.startswith(b'\x89PNG'), name)


# ---------------------------- авторизация ----------------------------

class LoginRedirectTest(TestCase):
    def setUp(self):
        make_client_user('login_user')

    def test_login_safe_next(self):
        response = self.client.post(
            reverse('login') + '?next=/tours/',
            {'username': 'login_user', 'password': 'pass12345'},
        )
        self.assertRedirects(response, '/tours/', fetch_redirect_response=False)

    def test_login_open_redirect_blocked(self):
        response = self.client.post(
            reverse('login') + '?next=https://evil.example.com/',
            {'username': 'login_user', 'password': 'pass12345'},
        )
        self.assertRedirects(response, reverse('profile'), fetch_redirect_response=False)

    def test_login_wrong_password(self):
        response = self.client.post(
            reverse('login'), {'username': 'login_user', 'password': 'wrong'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logged_in_user_redirected_from_login_and_register(self):
        self.client.login(username='login_user', password='pass12345')
        self.assertRedirects(self.client.get(reverse('login')), reverse('profile'),
                             fetch_redirect_response=False)
        self.assertRedirects(self.client.get(reverse('register')), reverse('profile'),
                             fetch_redirect_response=False)

    def test_logout_redirects_to_index(self):
        self.client.login(username='login_user', password='pass12345')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))


class RegistrationExtraTest(TestCase):
    def test_full_registration_creates_client_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'newbie', 'last_name': 'Новиков', 'first_name': 'Иван',
            'middle_name': '', 'address': 'г. Гомель', 'phone': '+375 (33) 123-45-67',
            'birth_date': '1995-04-04', 'timezone': 'Europe/Minsk',
            'password1': 'Str0ngPass!word', 'password2': 'Str0ngPass!word',
        })
        self.assertRedirects(response, reverse('profile'), fetch_redirect_response=False)
        self.assertTrue(Client.objects.filter(user__username='newbie').exists())


# ---------------------------- отзывы ----------------------------

class ReviewsExtraTest(TestCase):
    def test_employee_cannot_post_review(self):
        make_employee_user('rev_em')
        self.client.login(username='rev_em', password='pass12345')
        response = self.client.post(reverse('reviews'), {
            'author_name': 'x', 'text': 'текст', 'rating': 5,
        })
        self.assertRedirects(response, reverse('reviews'))
        self.assertEqual(Review.objects.count(), 0)

    def test_incomplete_review_not_saved(self):
        make_client_user('rev_cl')
        self.client.login(username='rev_cl', password='pass12345')
        self.client.post(reverse('reviews'), {'author_name': 'x', 'text': '', 'rating': 5})
        self.assertEqual(Review.objects.count(), 0)

    def test_review_page_shows_utc_and_slash_date(self):
        Review.objects.create(author_name='Аня', text='Супер', rating=5)
        response = self.client.get(reverse('reviews'))
        self.assertContains(response, 'UTC')
        self.assertContains(response, dj_timezone.now().strftime('%d/%m/%Y'))


# ---------------------------- даты, теги и модели ----------------------------

class DateTimeTagsTest(TestCase):
    def test_format_dual_aware(self):
        dt = datetime.datetime(2026, 1, 15, 9, 30, tzinfo=datetime.timezone.utc)
        result = format_dual(dt, 'Europe/Minsk')
        self.assertEqual(result, '15/01/2026 12:30 (Europe/Minsk) | 15/01/2026 09:30 UTC')

    def test_format_dual_naive_treated_as_utc(self):
        dt = datetime.datetime(2026, 1, 15, 9, 30)
        self.assertIn('15/01/2026 09:30 UTC', format_dual(dt, 'Europe/Minsk'))

    def test_format_dual_date_and_empty(self):
        self.assertEqual(format_dual(datetime.date(2026, 3, 4), 'Europe/Minsk'), '04/03/2026')
        self.assertEqual(format_dual(None, 'Europe/Minsk'), '')
        self.assertEqual(format_dual('abc', 'Europe/Minsk'), 'abc')

    def test_get_user_tz_name(self):
        self.assertEqual(get_user_tz_name(None), 'Europe/Minsk')
        self.assertEqual(get_user_tz_name(AnonymousUser()), 'Europe/Minsk')
        user, _ = make_client_user('tz_cl', tz='Asia/Tokyo')
        self.assertEqual(get_user_tz_name(user), 'Asia/Tokyo')
        em_user, _ = make_employee_user('tz_em', tz='Europe/London')
        self.assertEqual(get_user_tz_name(em_user), 'Europe/London')

    def test_news_and_index_show_both_timezones(self):
        News.objects.create(title='Заголовок', short_description='Кратко', content='Текст')
        for name in ('news_list', 'index'):
            response = self.client.get(reverse(name))
            self.assertContains(response, 'UTC')
            self.assertContains(response, dj_timezone.now().strftime('%d/%m/%Y'))

    def test_faq_shows_dates(self):
        FAQ.objects.create(question='Что такое виза?', answer='Разрешение на въезд')
        response = self.client.get(reverse('faq'))
        self.assertContains(response, 'Изменено')
        self.assertContains(response, 'UTC')


class ModelsExtraTest(TestCase):
    def test_updated_at_changes_on_save(self):
        faq = FAQ.objects.create(question='Q', answer='A')
        first = faq.updated_at
        faq.answer = 'B'
        faq.save()
        faq.refresh_from_db()
        self.assertGreaterEqual(faq.updated_at, first)
        self.assertIsNotNone(faq.created_at)

    def test_str_methods(self):
        country = make_country('Строка')
        hotel = make_hotel(country)
        tour = make_tour(hotel, title='Тур-строка')
        _, cl = make_client_user('str_cl')
        _, em = make_employee_user('str_em')
        order = make_order(cl, em, tour)
        self.assertEqual(str(country), 'Строка')
        self.assertIn('Тур-строка', str(tour))
        self.assertIn('Фамилияstr_cl', str(cl))
        self.assertIn('Менеджер', str(em))
        self.assertIn(str(order.id), str(order))
        self.assertEqual(str(News.objects.create(title='Н', short_description='к', content='т')), 'Н')


class HelpersTest(TestCase):
    def test_as_int_or_none(self):
        self.assertEqual(views.as_int_or_none('5'), 5)
        self.assertIsNone(views.as_int_or_none('abc'))
        self.assertIsNone(views.as_int_or_none(''))
        self.assertIsNone(views.as_int_or_none(None))

    def test_roles_and_labels(self):
        self.assertEqual(views.get_user_role(AnonymousUser()), 'guest')
        bare = User.objects.create_user('bare2', password='pass12345')
        self.assertEqual(views.get_user_role(bare), 'registered')
        self.assertEqual(views.get_role_label('client'), 'Клиент')
        self.assertEqual(views.get_role_label('unknown'), 'Пользователь')

    def test_about_page_with_company_info(self):
        CompanyInfo.objects.create(text='Мы лучшая компания')
        self.assertContains(self.client.get(reverse('about')), 'Мы лучшая компания')


# ==========================================================
# ЛР1 (HTML): новые страницы и функциональность
# ==========================================================
import datetime as _dt
from django.core.files.uploadedfile import SimpleUploadedFile
from agency.models import News, Inquiry, CompanyInfo, Banner, Country, Hotel, Client as _Client
from agency.forms import InquiryForm


class Lr1PagesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(title='Тест', short_description='Кратко.', content='Абзац 1\n\nАбзац 2')
        cls.country = Country.objects.create(
            name='Тестляндия', climate_winter='a', climate_spring='b', climate_summer='c', climate_autumn='d')
        Hotel.objects.create(country=cls.country, name='Отель', stars=4, price_per_day=100)

    def test_news_detail(self):
        r = self.client.get(f'/news/{self.news.pk}/')
        self.assertContains(r, 'Абзац 2')
        self.assertContains(r, 'Все новости')

    def test_news_detail_404(self):
        self.assertEqual(self.client.get('/news/9999/').status_code, 404)

    def test_news_list_has_read_more(self):
        r = self.client.get('/news/')
        self.assertContains(r, 'Читать далее')
        self.assertContains(r, f'/news/{self.news.pk}/')

    def test_guide_page_has_semantic_examples(self):
        r = self.client.get('/guide/')
        self.assertEqual(r.status_code, 200)
        for tag in ('<abbr', '<dfn', '<blockquote', '<pre', '<audio', '<video', '<iframe',
                    'srcset=', '<picture', '<wbr>', 'download'):
            self.assertContains(r, tag)

    def test_price_list_table(self):
        r = self.client.get('/prices/')
        self.assertContains(r, 'rowspan')
        self.assertContains(r, 'headers=')
        self.assertContains(r, '700')  # 100 * 7

    def test_price_list_empty(self):
        Hotel.objects.all().delete()
        self.assertContains(self.client.get('/prices/'), 'Отели пока не добавлены')

    def test_privacy_has_content(self):
        self.assertContains(self.client.get('/privacy/'), 'Права пользователя')

    def test_faq_uses_details(self):
        FAQ.objects.create(question='Что такое ваучер?', answer='Документ.')
        r = self.client.get('/faq/')
        self.assertContains(r, '<details')
        self.assertContains(r, '<summary')

    def test_no_css_files_or_classes(self):
        for url in ('/', '/about/', '/news/', '/guide/', '/prices/', '/request/', '/login/', '/register/', '/tours/'):
            html = self.client.get(url).content.decode()
            self.assertNotIn('rel="stylesheet"', html, url)
            self.assertNotIn('<style', html, url)
            self.assertNotIn(' class=', html, url)

    def test_about_parses_company_info(self):
        CompanyInfo.objects.create(
            text='Текст', history_by_years='2010 — старт\n2020 — рост', requisites='УНП: 123\nБанк: Б',
            certificate_text='Свидетельство\nНомер 1')
        r = self.client.get('/about/')
        self.assertContains(r, '2010')
        self.assertContains(r, 'УНП')
        self.assertContains(r, 'Свидетельство')

    def test_about_without_company_info(self):
        r = self.client.get('/about/')
        self.assertContains(r, 'История компании пока не добавлена')

    def test_about_with_line_without_separator(self):
        CompanyInfo.objects.create(text='t', history_by_years='без разделителя')
        self.assertContains(self.client.get('/about/'), 'без разделителя')

    def test_contacts_show_description(self):
        user = User.objects.create_user('emp1', password='x')
        Employee.objects.create(user=user, full_name='Иван Иванов', position='Менеджер',
                                phone='+375 (29) 111-22-33', email='i@e.by',
                                birth_date=_dt.date(1990, 1, 1), description='Подбирает туры')
        self.assertContains(self.client.get('/contacts/'), 'Подбирает туры')


class Lr1BannerTest(TestCase):
    def test_banner_uses_different_images_per_breakpoint(self):
        Banner.objects.create(title='B', image='banners/d.jpg', image_tablet='banners/t.jpg',
                              image_mobile='banners/m.jpg')
        r = self.client.get('/')
        self.assertContains(r, '<picture>')
        self.assertContains(r, 'banners/m.jpg')
        self.assertContains(r, 'banners/t.jpg')
        self.assertContains(r, 'banners/d.jpg')

    def test_banner_without_variants(self):
        Banner.objects.create(title='B', image='banners/d.jpg')
        r = self.client.get('/')
        self.assertContains(r, 'banners/d.jpg')
        self.assertNotContains(r, 'max-width: 600px')

    def test_latest_news_on_home_has_link(self):
        n = News.objects.create(title='Свежая', short_description='s', content='c')
        self.assertContains(self.client.get('/'), f'/news/{n.pk}/')


class Lr1InquiryTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            name='Страна', climate_winter='a', climate_spring='b', climate_summer='c', climate_autumn='d')
        self.valid = {
            'name': 'Пётр', 'email': 'p@example.com', 'phone': '+375 (29) 123-45-67',
            'country': self.country.pk, 'departure_city': 'Минск',
            'departure_date': (_dt.date.today() + _dt.timedelta(days=10)).isoformat(),
            'adults': 2, 'meal_plan': 'AI', 'budget': 1500, 'contact_method': 'email', 'agree': 'on',
        }

    def test_get_form(self):
        r = self.client.get('/request/')
        self.assertContains(r, 'type="range"')
        self.assertContains(r, '<datalist')
        self.assertContains(r, 'type="radio"')
        self.assertContains(r, 'type="time"')

    def test_valid_submit_saves(self):
        r = self.client.post('/request/', self.valid)
        self.assertRedirects(r, '/request/')
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertIn('Пётр', str(Inquiry.objects.first()))

    def test_invalid_phone(self):
        r = self.client.post('/request/', {**self.valid, 'phone': '123'})
        self.assertEqual(Inquiry.objects.count(), 0)
        self.assertContains(r, 'Номер телефона должен быть')

    def test_past_date_rejected(self):
        r = self.client.post('/request/', {**self.valid, 'departure_date': '2000-01-01'})
        self.assertContains(r, 'не может быть в прошлом')

    def test_adults_range(self):
        r = self.client.post('/request/', {**self.valid, 'adults': 50})
        self.assertContains(r, 'от 1 до 10')

    def test_budget_min(self):
        r = self.client.post('/request/', {**self.valid, 'budget': 10})
        self.assertContains(r, 'Минимальный бюджет')

    def test_consent_required(self):
        data = dict(self.valid); data.pop('agree')
        self.client.post('/request/', data)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_form_clean_methods_directly(self):
        form = InquiryForm(data={**self.valid, 'adults': 0})
        self.assertFalse(form.is_valid())
        self.assertIn('adults', form.errors)


class Lr1ReviewFlowTest(TestCase):
    def test_review_button_for_guest_leads_to_register(self):
        self.assertContains(self.client.get('/reviews/'), 'href="/register/"')

    def test_review_button_for_user_leads_to_profile(self):
        u = User.objects.create_user('someone', password='x')
        self.client.force_login(u)
        self.assertContains(self.client.get('/reviews/'), '/profile/?review=1#review-form')

    def test_profile_of_client_has_review_form(self):
        u = User.objects.create_user('cl', password='x')
        _Client.objects.create(user=u, last_name='Л', first_name='И', address='а',
                               phone='+375 (29) 111-11-11', birth_date=_dt.date(1990, 1, 1))
        self.client.force_login(u)
        r = self.client.get('/profile/?review=1')
        self.assertContains(r, 'id="review-form"')
        self.assertContains(r, 'Отправить')
        self.client.post('/reviews/', {'author_name': 'cl', 'rating': 5, 'text': 'Отличная поездка!'})
        self.assertEqual(Review.objects.filter(user=u).count(), 1)


class Lr1FormStylesTest(TestCase):
    def test_login_fields_have_inline_style(self):
        self.assertContains(self.client.get('/login/'), 'style="width: 100%')

    def test_register_fields_have_inline_style(self):
        self.assertContains(self.client.get('/register/'), 'box-sizing: border-box')
