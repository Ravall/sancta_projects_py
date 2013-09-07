# -*- coding: utf-8 -*-
# pylint: disable=W0613, W0622
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from mf_system.models import MfSystemArticle
from api.models import prepare_article, prepare_articles
from api.decorator import responsed, cached_result


@api_view(['GET'])
@responsed
@cached_result('article-api')
def get_articles(request, site_name, article_id, format):
    try:
        params = {
            'status': 'active',
            'id' if article_id.isdigit() else 'url': article_id,
            'site__name': site_name
        }
        article = MfSystemArticle.objects.get(**params)
    except ObjectDoesNotExist:
        return False
    return prepare_article(article, add_related=True)


@api_view(['GET'])
@responsed
@cached_result('articletag-api')
def get_articles_by_tag(request, site_name, article_tag, format):
    articles = MfSystemArticle.objects.filter(
        tags__name__in=[article_tag],
        status='active',
        site__name=site_name
    ).order_by('order')
    if not articles:
        return False
    return prepare_articles(articles)
