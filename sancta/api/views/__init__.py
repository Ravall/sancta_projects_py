# -*- coding: utf-8 -*-
# pylint: disable=W0613, W0622
from __future__ import unicode_literals
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_example(request, format):
    resource_urls = [
        reverse(
            'event-api', kwargs={'event_id': 29, 'format': 'json'},
            request=request
        ),
        reverse(
            'eventall-api', kwargs={'format': 'json'},
            request=request
        ),
        reverse(
            'article-api',
            kwargs={
                'site_name': 'orthodoxy',
                'article_id': 231,
                'format': 'json'
            },
            request=request
        ),
        reverse(
            'articletag-api',
            kwargs={
                'site_name': 'orthodoxy',
                'article_tag': 'post',
                'format': 'json'
            },
            request=request
        ),
        reverse(
            'calendar-api', kwargs={'day': '2012-10-14', 'format': 'json'},
            request=request
        )
    ]
    return Response({"example": resource_urls})
