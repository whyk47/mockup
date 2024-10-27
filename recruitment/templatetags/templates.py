from django.template import Library

register = Library()

@register.filter
def div(x: str |int | float, y: str | int | float) -> str:
    q = float(x) / float(y)
    return f'{q:.1f}'