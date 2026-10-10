from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

from .models import Client, Tour, Inquiry, phone_validator, validate_adult

import pytz
TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]


INPUT_STYLE = ('width: 100%; box-sizing: border-box; padding: 8px; border: 1px solid #ccc; '
               'border-radius: 4px; margin-bottom: 10px; font-family: inherit;')


def apply_inline_styles(form):
    """Внешнего CSS нет: поля, которые рисует Django, получают стиль атрибутом style."""
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.HiddenInput)):
            continue
        widget.attrs.setdefault('style', INPUT_STYLE)


class InlineStyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_inline_styles(self)


class StyledAuthenticationForm(InlineStyledFormMixin, AuthenticationForm):
    """Форма входа с inline-стилями полей."""


class TourForm(InlineStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['hotel', 'title', 'duration_weeks', 'departure_date', 'is_hot']
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ClientRegistrationForm(InlineStyledFormMixin, UserCreationForm):
    last_name = forms.CharField(
        label="Фамилия",
        max_length=100,
    )
    first_name = forms.CharField(
        label="Имя",
        max_length=100,
    )
    middle_name = forms.CharField(
        label="Отчество",
        max_length=100,
        required=False,
    )
    address = forms.CharField(
        label="Адрес",
        max_length=255,
    )

    timezone = forms.ChoiceField(
        label="Ваша тайм-зона",
        choices=TIMEZONE_CHOICES,
        initial='Europe/Minsk',
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        help_text="Формат: +375 (29) XXX-XX-XX. Допустимые коды: 25, 29, 33, 44.",
        widget=forms.TextInput(attrs={'placeholder': '+375 (29) XXX-XX-XX'}),
    )
    birth_date = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Регистрация доступна только клиентам 18+.",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'last_name', 'first_name', 'middle_name',
            'address', 'phone', 'birth_date', 'timezone',
            'password1', 'password2',
        )

    def clean_phone(self):
        """Валидируем телефон напрямую через валидатор из модели."""
        phone = self.cleaned_data.get('phone', '').strip()
        try:
            phone_validator(phone)
        except ValidationError as e:
            raise ValidationError(e.message)
        return phone

    def clean_birth_date(self):
        """Валидируем возраст 18+ напрямую через валидатор из модели."""
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            try:
                validate_adult(birth_date)
            except ValidationError as e:
                raise ValidationError(e.message)
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Client.objects.create(
                user=user,
                last_name=self.cleaned_data['last_name'],
                first_name=self.cleaned_data['first_name'],
                middle_name=self.cleaned_data.get('middle_name') or '',
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone'],
                birth_date=self.cleaned_data['birth_date'],
                timezone=self.cleaned_data['timezone'],
            )
        return user


class InquiryForm(forms.ModelForm):
    """Заявка на подбор тура. Валидация на сервере дублирует клиентскую (HTML5)."""
    agree = forms.BooleanField(label="Согласен на обработку персональных данных")

    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'country', 'departure_city', 'departure_date',
                  'adults', 'with_children', 'meal_plan', 'budget', 'contact_method',
                  'call_time', 'comment']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        phone_validator(phone)
        return phone

    def clean_departure_date(self):
        date = self.cleaned_data['departure_date']
        if date < datetime.date.today():
            raise ValidationError("Дата вылета не может быть в прошлом.")
        return date

    def clean_adults(self):
        adults = self.cleaned_data['adults']
        if not 1 <= adults <= 10:
            raise ValidationError("Количество взрослых — от 1 до 10.")
        return adults

    def clean_budget(self):
        budget = self.cleaned_data['budget']
        if budget < 100:
            raise ValidationError("Минимальный бюджет — 100 BYN.")
        return budget
