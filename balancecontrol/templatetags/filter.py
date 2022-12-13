from django.template import Library
from utils import utils

register = Library()


@register.filter
def value_format(val):
    return utils.value_format(val)
