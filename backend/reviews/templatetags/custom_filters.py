# myapp/templatetags/custom_filters.py
from django import template
from decimal import Decimal, ROUND_HALF_UP

register = template.Library()

@register.filter
def star_rating(value):
    if value is None:
        return ''
    # 小数第3位で四捨五入 → 整数に
    rounded = int(Decimal(value).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    return '★' * rounded + '☆' * (5 - rounded)