# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
import requests

API_URL = 'http://api.sancta.ru/api/'

def get_article(request, article):
    r = requests.get(
        '{0}article/{1}.{2}'.format(
            API_URL, 'klassifikaciya_prazdnikov_v_pravoslavii', 'json'
        )
    )
    r.raise_for_status()
    return render_to_response(
        'orthcalendar/article.html',
        {'article': r.json()},
        context_instance=RequestContext(request)
    )