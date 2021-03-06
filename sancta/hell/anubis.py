# -*- coding: utf-8 -*-
# pylint: disable=E1102,R0201
'''
Анубис - проводник в мир мертвых
-----
   создает sitemap.xml для orthcalendar
'''
import celery
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpRequest
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from mf_calendar import models as calendar_model
from mf_system import models as system_model
from smart_date.smartfunction import smart_function
from smart_date.date import yyyy_mm_dd


class ObjSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def lastmod(self, obj):
        return obj['lastmod']

    def location(self, obj):
        return obj['location']


class EventSitemap(ObjSitemap):
    """
    карта событий и икон к ним
    """
    def items(self):
        events = calendar_model.MfCalendarEvent.objects.filter(
            status='active',
        )
        links = []
        for event in events:
            links.append(dict(
                lastmod=event.updated,
                location='/event/{0}'.format(event.id)
            ))
            if event.count_icons > 0:
                links.append(dict(
                    lastmod=event.updated,
                    location='/event/{0}/icons'.format(event.url)
                ))
        return links


class ArticleSitemap(ObjSitemap):
    """
    карта статей
    """
    def items(self):
        articles = system_model.MfSystemArticle.objects.filter(
            status='active',
        )
        return [
            dict(
                lastmod=art.updated,
                location='/article/{0}'.format(art.id)
            ) for art in articles
        ]


class CalendarNetSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    lastmod = datetime.now() - timedelta(1)

    def location(self, obj):
        return obj

    def items(self):
        date_from = yyyy_mm_dd(smart_function('01.01.-1', None)[0])
        date_to = yyyy_mm_dd(smart_function('31.12.+1', None)[0])
        net = calendar_model.MfCalendarNet.objects.filter(
            full_date__gte=date_from,
            full_date__lte=date_to
        )
        return ['/orthodoxy/{0}'.format(n.full_date) for n in net]


class SimplePages(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    lastmod = None

    def location(self, obj):
        return obj

    def items(self):
        return [
            '/about',
            '/event/all',
            '/contact',
            '/donate',
        ]


class Anubis():
    name = 'anubis'

    def __init__(self):
        self.logger = logging.getLogger('sancta_log')

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.name, message))

    def generate_sitemap(self):
        self.log("start")
        sitemaps = {
            'events': EventSitemap(),
            'articles': ArticleSitemap(),
            'net': CalendarNetSitemap(),
            'simple': SimplePages()
        }
        self.log("generate sitemap")
        self.log(
            "events: {0} links".format(sitemaps['events'].paginator.count)
        )
        self.log(
            "articles: {0} links".format(sitemaps['articles'].paginator.count)
        )
        self.log(
            "net: {0} links".format(sitemaps['net'].paginator.count)
        )
        self.log(
            "simple: {0} links".format(sitemaps['simple'].paginator.count)
        )
        xml = sitemap(HttpRequest(), sitemaps)
        xml_file = open(settings.SITEMAP, 'w')
        self.log("write to {0}".format(settings.SITEMAP))
        xml_file.write(xml.rendered_content.encode("utf-8"))
        xml_file.close()
        self.log("finish")


@celery.task()
def generate_sitemap_file():
    daemon = Anubis()
    daemon.generate_sitemap()
