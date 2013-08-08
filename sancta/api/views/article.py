# -*- coding: utf-8 -*-
# pylint: disable=W0613, W0622
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import get_cache
from django.conf import settings
from mf_system.models import MfSystemArticle
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.reverse import reverse
from api.models import prepare_article, prepare_articles


@api_view(['GET'])
def get_articles(request, site_name, article_id, format):
    """
    возвращает информацию о статьях
    """
    if settings.IS_TESTING:
        result = False
    else:
        cache = get_cache('api')
        cache_key = reverse(
            'article-api', kwargs={
                'site_name': site_name,
                'article_id': article_id,
                'format': format
            }
        )
        result = cache.get(cache_key)
    if not result:
        try:
            params = {
                'status': 'active',
                'id' if article_id.isdigit() else 'url': article_id,
                'site__name': site_name
            }
            article = MfSystemArticle.objects.get(**params)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        result = prepare_article(article, add_related=True)
        if not settings.IS_TESTING:
            cache.set(cache_key, result, 30)
    return Response(result)


@api_view(['GET'])
def get_articles_by_tag(request, site_name, article_tag, format):
    articles = MfSystemArticle.objects.filter(
        tags__name__in=[article_tag],
        status='active',
        site__name=site_name
    )
    if not articles:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(prepare_articles(articles))
