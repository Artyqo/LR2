from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
import pytz

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]

# ==========================================
# ВАЛИДАТОРЫ
# ==========================================

# 1. Валидатор телефона по маске +375 (29) XXX-XX-XX
phone_validator = RegexValidator(
    regex=r'^\+375 \((25|29|33|44)\) \d{3}-\d{2}-\d{2}$',
    message="Номер телефона должен быть в формате: +375 (29) XXX-XX-XX. Допустимые коды: 25, 29, 33, 44."
)

# 2. Валидатор возраста 18+
def validate_adult(birth_date):
    if birth_date:
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise ValidationError("Возраст должен быть не менее 18 лет.")


# ======================
# БЛОК 1: ОБЩИЕ МОДЕЛИ
# =====================

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_description = models.CharField(max_length=250, verbose_name="Краткое содержание (одно предложение)")
    content = models.TextField(verbose_name="Полное содержание статьи")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="Картинка")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class CompanyInfo(models.Model):
    text = models.TextField(verbose_name="Информация о компании (просто текст)")
    logo = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name="Логотип (***)")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео (***)")
    video_file = models.FileField(upload_to='company/', blank=True, null=True, verbose_name="Видеофайл о компании")
    history_by_years = models.TextField(blank=True, null=True, verbose_name="История по годам (***)")
    requisites = models.TextField(blank=True, null=True, verbose_name="Реквизиты (***)")
    certificate_text = models.TextField(blank=True, null=True, verbose_name="Сертификат (текст)")

    class Meta:
        verbose_name = "О компании"
        verbose_name_plural = "О компании"


class FAQ(models.Model):
    question = models.CharField(max_length=250, verbose_name="Вопрос / Термин")
    answer = models.TextField(verbose_name="Ответ / Определение")
    date_added = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Добавлено (дата и время)")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Термин/Вопрос"
        verbose_name_plural = "Словарь терминов и понятий"


class Vacancy(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание вакансии")
    salary = models.CharField(max_length=100, blank=True, null=True, verbose_name="Заработная плата")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    author_name = models.CharField(max_length=100, verbose_name="Имя автора (если не зарегистрирован)")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Оценка")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    discount_amount = models.IntegerField(verbose_name="Размер скидки (в %)")
    is_active = models.BooleanField(default=True, verbose_name="Действующий (иначе в архиве)")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды и купоны"

    def __str__(self):
        return f"{self.code} ({'Активен' if self.is_active else 'Архив'})"


# ==========================================
# БЛОК 2: СУЩНОСТИ ВАРИАНТА №4 (ТУРАГЕНТСТВО)
# ==========================================

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название страны")
    climate_winter = models.CharField(max_length=150, verbose_name="Климат зимой")
    climate_spring = models.CharField(max_length=150, verbose_name="Климат весной")
    climate_summer = models.CharField(max_length=150, verbose_name="Климат летом")
    climate_autumn = models.CharField(max_length=150, verbose_name="Климат осенью")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Hotel(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="hotels", verbose_name="Страна")
    name = models.CharField(max_length=150, verbose_name="Название отеля")
    stars = models.IntegerField(choices=[(i, '★' * i) for i in range(1, 6)], verbose_name="Количество звезд")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость в сутки")
    latitude = models.FloatField(blank=True, null=True, verbose_name="Широта для карты (***)")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Долгота для карты (***)")

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"

    def __str__(self):
        return f"{self.name} { '★' * self.stars }"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile", verbose_name="Аккаунт Django")
    full_name = models.CharField(max_length=200, verbose_name="ФИО сотрудника")
    position = models.CharField(max_length=100, verbose_name="Должность")
    # Добавлены валидаторы телефона и возраста
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name="Телефон")
    birth_date = models.DateField(validators=[validate_adult], null=True, blank=False, verbose_name="Дата рождения (18+)")
    timezone = models.CharField(
        max_length=50,
        default='Europe/Minsk',
        choices=TIMEZONE_CHOICES,
        verbose_name="Тайм-зона",
    )
    email = models.EmailField(verbose_name="Почта")
    description = models.TextField(blank=True, default='', verbose_name="Описание выполняемых работ")
    photo = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name="Фото сотрудника")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.full_name} ({self.position})"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile", verbose_name="Аккаунт Django")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    # Добавлены валидаторы телефона и возраста
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name="Телефон")
    birth_date = models.DateField(validators=[validate_adult], null=True, blank=False, verbose_name="Дата рождения (18+)")
    timezone = models.CharField(
        max_length=50,
        default='Europe/Minsk',
        choices=TIMEZONE_CHOICES,
        verbose_name="Тайм-зона",
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Tour(models.Model):
    DURATION_CHOICES = [
        (1, '1 неделя'),
        (2, '2 недели'),
        (4, '4 недели'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="tours", verbose_name="Отель")
    title = models.CharField(max_length=200, verbose_name="Название путевки/направления")
    duration_weeks = models.IntegerField(choices=DURATION_CHOICES, verbose_name="Длительность (в неделях)")
    departure_date = models.DateField(verbose_name="Дата отправления")
    is_hot = models.BooleanField(default=False, verbose_name="Горящая путевка")
    description = models.TextField(blank=True, default='', verbose_name="Описание путёвки")
    image = models.ImageField(upload_to='tours/', blank=True, null=True, verbose_name="Картинка путёвки")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    @property
    def price(self):
        days = self.duration_weeks * 7
        return self.hotel.price_per_day * days

    class Meta:
        verbose_name = "Путевка"
        verbose_name_plural = "Путевки"

    def __str__(self):
        return f"{self.title} ({self.get_duration_weeks_display()}) — {self.price} руб."


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders", verbose_name="Клиент")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="orders_handled", verbose_name="Сотрудник, оформивший заказ")
    tours = models.ManyToManyField(Tour, related_name="orders", verbose_name="Выбранные путевки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оформления заказа")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Итоговая стоимость")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} ({self.client})"

# ==========================================================
# ЛР1: ПАРТНЁРЫ, БАННЕРЫ, КОРЗИНА, ПОЗИЦИИ ЗАКАЗА
# ==========================================================

class Partner(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название компании")
    logo = models.ImageField(upload_to='partners/', verbose_name="Логотип")
    website = models.URLField(verbose_name="Сайт компании")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок показа")
    is_active = models.BooleanField(default=True, verbose_name="Показывать на сайте")

    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Banner(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок (alt-текст)")
    image = models.ImageField(upload_to='banners/', verbose_name="Изображение баннера (десктоп)")
    image_tablet = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name="Изображение для планшета (до 992 px)")
    image_mobile = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name="Изображение для телефона (до 600 px)")
    link_url = models.CharField(max_length=200, blank=True, default='', verbose_name="Ссылка (например, /tours/)")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок показа")
    is_active = models.BooleanField(default=True, verbose_name="Показывать на сайте")

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title


class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="cart", verbose_name="Клиент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменена")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    @property
    def total(self):
        return sum((item.subtotal for item in self.items.select_related('tour__hotel')), 0)

    @property
    def items_count(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Корзина: {self.client}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Корзина")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Путёвка")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"
        constraints = [
            models.UniqueConstraint(fields=['cart', 'tour'], name='unique_tour_in_cart'),
        ]

    @property
    def subtotal(self):
        return self.tour.price * self.quantity

    def __str__(self):
        return f"{self.tour.title} × {self.quantity}"


class OrderItem(models.Model):
    """Позиция заказа: путёвка, количество и цена на момент оплаты."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="order_items", verbose_name="Путёвка")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Количество")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена за единицу")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.tour.title} × {self.quantity}"


class Inquiry(models.Model):
    """Заявка на подбор тура (форма с разными элементами управления)."""
    CONTACT_CHOICES = [('phone', 'По телефону'), ('email', 'По e-mail')]
    MEAL_CHOICES = [('RO', 'Без питания'), ('BB', 'Завтраки'), ('HB', 'Полупансион'), ('AI', 'Всё включено')]
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name="Телефон")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="inquiries", verbose_name="Желаемая страна")
    departure_date = models.DateField(verbose_name="Желаемая дата вылета")
    adults = models.PositiveSmallIntegerField(default=1, verbose_name="Количество взрослых")
    budget = models.PositiveIntegerField(default=1000, verbose_name="Бюджет, BYN")
    departure_city = models.CharField(max_length=60, blank=True, default='', verbose_name="Город вылета")
    meal_plan = models.CharField(max_length=2, choices=MEAL_CHOICES, default='BB', verbose_name="Тип питания")
    with_children = models.BooleanField(default=False, verbose_name="Поездка с детьми")
    contact_method = models.CharField(max_length=10, choices=CONTACT_CHOICES, default='phone',
                                      verbose_name="Способ связи")
    call_time = models.TimeField(null=True, blank=True, verbose_name="Удобное время звонка")
    comment = models.TextField(blank=True, default='', verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")

    class Meta:
        verbose_name = "Заявка на подбор тура"
        verbose_name_plural = "Заявки на подбор тура"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.name} ({self.departure_date:%d/%m/%Y})"
