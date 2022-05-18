from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    return float(value) - float(arg)


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter
def find_percent(change_today):
    return round(float(change_today)*100, 2)


@register.filter
def compare(value, arg):
    if float(value) > float(arg):
        return True
