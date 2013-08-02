# -*- coding: utf-8 -*-
# pylint: disable=W0613, W0622
from django.core.exceptions import ObjectDoesNotExist
from mf_system.models import MfSystemArticle
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import prepare_article, prepare_articles


@api_view(['GET'])
def get_articles(request, site_name, article_id, format):
    """
    возвращает информацию о статьях
    """
    try:
        params = {
            'status': 'active',
            'id' if article_id.isdigit() else 'url': article_id,
            'site__name': site_name
        }
        article = MfSystemArticle.objects.get(**params)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(prepare_article(article, add_related=True))


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
