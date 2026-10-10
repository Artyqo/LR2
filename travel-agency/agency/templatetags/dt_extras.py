"""Теги для вывода даты/времени в формате DD/MM/YYYY: в тайм-зоне пользователя и в UTC."""
import datetime

import pytz
from django import template
from django.utils import timezone as dj_timezone

register = template.Library()

DEFAULT_TZ = 'Europe/Minsk'
FMT = '%d/%m/%Y %H:%M'


def get_user_tz_name(user):
    """Тайм-зона пользователя из профиля клиента/сотрудника; для остальных — Europe/Minsk."""
    if user is not None and getattr(user, 'is_authenticated', False):
        for attr in ('client_profile', 'employee_profile'):
            profile = getattr(user, attr, None)
            if profile is not None and getattr(profile, 'timezone', None):
                return profile.timezone
    return DEFAULT_TZ


def format_dual(value, tz_name):
    """Возвращает строку вида '28/09/2026 12:00 (Europe/Minsk) | 28/09/2026 09:00 UTC'."""
    if value is None or value == '':
        return ''
    if isinstance(value, datetime.datetime):
        if dj_timezone.is_naive(value):
            value = pytz.utc.localize(value)
        local = value.astimezone(pytz.timezone(tz_name))
        utc = value.astimezone(pytz.utc)
        return f'{local.strftime(FMT)} ({tz_name}) | {utc.strftime(FMT)} UTC'
    if isinstance(value, datetime.date):
        return value.strftime('%d/%m/%Y')
    return str(value)


@register.simple_tag(takes_context=True)
def dt_dual(context, value):
    """{% dt_dual obj.updated_at %} — дата в тайм-зоне пользователя и в UTC."""
    request = context.get('request')
    user = getattr(request, 'user', None)
    return format_dual(value, get_user_tz_name(user))
