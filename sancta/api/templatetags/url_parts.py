# -*- coding: utf-8 -*-
# pylint: disable=C0103
from django import template


register = template.Library()


@register.filter
def url_parts(url, part):
    return url.split('/')[part]
