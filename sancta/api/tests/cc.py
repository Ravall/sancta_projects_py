# -*- coding: utf-8 -*-
from django.test import TestCase
from mock import patch, call
from hell import sabnac
from mf_system.models.mf_article import MfSystemArticle
from mf_calendar.models import MfCalendarEvent, MfCalendarIcon


class CcCase(TestCase):
    fixtures = [
        'mf_system_relation_type.yaml',
        'mf_calendar_smart_function.yaml',
        'mf_system_object.yaml',
        'mf_calendar_event.yaml',
        'mf_calendar_icon.yaml',
        'mf_system_article.yaml',
        'mf_system_text.yaml',
        'mf_system_object_text.yaml',
        'mf_system_relation.yaml',
        'mf_calendar_net.yaml'
    ]


class CcArticleTest(CcCase):
    @staticmethod
    def get_cleaned_data():
        return {
            'title': 'title',
            'content': 'content',
            'annonce': 'annonce',
            'status': 'active',
            'tags': '',
            'created': '',
            'updated': '',
            'created_class': 'MfSystemArticle',
            'site': 1,
            'seo_url': 'seo_url'
        }

    def test_create_article(self):
        cleaned_data = self.get_cleaned_data()
        with patch(
            "api.cc._remove_cach_file_by_url", return_value=1
        ) as mock_cc:
            sabnac.update_article(MfSystemArticle(), cleaned_data)
            self.assertEquals(mock_cc.mock_calls, [
                call('/api/article/seo_url.json'),
                call('/api/article/seo_url.xml')
            ])
        #проверим теги
        cleaned_data['tags'] = 'xxx, yyy,'
        with patch(
            "api.cc._remove_cach_file_by_url", return_value=1
        ) as mock_cc:
            sabnac.update_article(MfSystemArticle(), cleaned_data)
            self.assertEquals(mock_cc.mock_calls, [
                call('/api/article/tag/xxx.json'),
                call('/api/article/tag/xxx.xml'),
                call('/api/article/tag/yyy.json'),
                call('/api/article/tag/yyy.xml'),
                call('/api/article/seo_url.json'),
                call('/api/article/seo_url.xml')
            ])

    def test_upd_ex_unrelated_article(self):
        """
        обновляем непривязанную статью
        """
        cleaned_data = self.get_cleaned_data()
        cleaned_data['tags'] = 'tag1, tag2'
        article = MfSystemArticle.objects.get(pk=377)
        article.tags.add('old_tag1', 'old_tag2')
        with patch(
            "api.cc._remove_cach_file_by_url", return_value=1
        ) as mock_cc:
            sabnac.update_article(article, cleaned_data)
            self.assertEquals(mock_cc.mock_calls, [
                call('/api/article/article_50_1.json'),
                call('/api/article/article_50_1.xml'),
                call('/api/article/377.json'),
                call('/api/article/377.xml'),
                #почему-то такой порядок
                call('/api/article/tag/old_tag2.json'),
                call('/api/article/tag/old_tag2.xml'),
                call('/api/article/tag/old_tag1.json'),
                call('/api/article/tag/old_tag1.xml'),
                call('/api/article/tag/tag1.json'),
                call('/api/article/tag/tag1.xml'),
                call('/api/article/tag/tag2.json'),
                call('/api/article/tag/tag2.xml'),
                call('/api/article/seo_url.json'),
                call('/api/article/seo_url.xml'),
            ])

    def test_upd_ex_related_article(self):
        """
        обновляем привязанную статью
        """
        article = MfSystemArticle.objects.get(pk=374)
        with patch(
            "api.cc._remove_cach_file_by_url", return_value=1
        ) as mock_cc:
            sabnac.update_article(article, self.get_cleaned_data())
            self.assertEquals(mock_cc.mock_calls, [
                # урл старый
                call('/api/article/article_14_2.json'),
                call('/api/article/article_14_2.xml'),
                # id статьи
                call('/api/article/374.json'),
                call('/api/article/374.xml'),
                # calendar/(все даты по smart_function события,
                # к которому привязана статья)
                call('/api/calendar/2010-04-07.json'),
                call('/api/calendar/2010-04-07.xml'),
                call('/api/calendar/2011-04-07.json'),
                call('/api/calendar/2011-04-07.xml'),
                # event/[id к которому привязана статья]
                call('/api/event/14.json'),
                call('/api/event/14.xml'),
                # event/[url к которому привязана статья]
                call('/api/event/blagoveshenie_presvyatoy_bogorodicy.json'),
                call('/api/event/blagoveshenie_presvyatoy_bogorodicy.xml'),
                # урл новый
                call('/api/article/seo_url.json'),
                call('/api/article/seo_url.xml')
            ])


class CcEventTest(CcCase):
    @staticmethod
    def get_cleaned_data():
        return {
            'title': 'title',
            'content': 'content',
            'annonce': 'annonce',
            'status': 'active',
            'periodic': 0,
            'smart_function': '01.01',
            'add_article': '',
            'tags': '',
            'created': '',
            'updated': '',
            'created_class': 'MfSystemArticle',
            'site': 1,
            'seo_url': 'seo_url',
            'icon_title': ''
        }

    def test_create_event(self):
        """
        тестируем создание событий
        Теги не используем - пока не предусмотренно.
        """
        cleaned_data = self.get_cleaned_data()
        with patch(
            "api.cc._remove_cach_file_by_url", return_value=1
        ) as mock_cc:
            sabnac.update_event(MfCalendarEvent(), cleaned_data)
            self.assertEquals(mock_cc.mock_calls, [
                call('/api/event/seo_url.json'),
                call('/api/event/seo_url.xml'),
                call('/api/calendar/2010-01-01.json'),
                call('/api/calendar/2010-01-01.xml'),
                call('/api/calendar/2011-01-01.json'),
                call('/api/calendar/2011-01-01.xml'),
            ])

    def test_upd_ex_event(self):
        cleaned_data = self.get_cleaned_data()
        event = MfCalendarEvent.objects.get(pk=27)
        with patch(
            "api.cc._remove_cach_file_by_url", return_value=1
        ) as mock_cc:
            sabnac.update_event(event, cleaned_data)
            self.assertEquals(mock_cc.mock_calls, [
                call('/api/event/27.json'),
                call('/api/event/27.xml'),
                call('/api/event/velikiy_post.json'),
                call('/api/event/velikiy_post.xml'),
                call('/api/calendar/2010-02-02.json'),
                call('/api/calendar/2010-02-02.xml'),
                call('/api/calendar/2011-02-02.json'),
                call('/api/calendar/2011-02-02.xml'),
                call('/api/event/seo_url.json'),
                call('/api/event/seo_url.xml'),
                call('/api/calendar/2010-01-01.json'),
                call('/api/calendar/2010-01-01.xml'),
                call('/api/calendar/2011-01-01.json'),
                call('/api/calendar/2011-01-01.xml'),
            ])

    def test_event_with_articles(self):
        cleaned_data = self.get_cleaned_data()
        event = MfCalendarEvent.objects.get(pk=14)
        with patch(
            "api.cc._remove_cach_file_by_url", return_value=1
        ) as mock_cc:
            sabnac.update_event(event, cleaned_data)
            self.assertEquals(mock_cc.mock_calls, [
                call('/api/event/14.json'),
                call('/api/event/14.xml'),
                call('/api/event/blagoveshenie_presvyatoy_bogorodicy.json'),
                call('/api/event/blagoveshenie_presvyatoy_bogorodicy.xml'),
                call('/api/calendar/2010-04-07.json'),
                call('/api/calendar/2010-04-07.xml'),
                call('/api/calendar/2011-04-07.json'),
                call('/api/calendar/2011-04-07.xml'),
                call('/api/event/seo_url.json'),
                call('/api/event/seo_url.xml'),
                call('/api/calendar/2010-01-01.json'),
                call('/api/calendar/2010-01-01.xml'),
                call('/api/calendar/2011-01-01.json'),
                call('/api/calendar/2011-01-01.xml'),
                call('/api/article/article_14_1.json'),
                call('/api/article/article_14_1.xml'),
                call('/api/article/373.json'),
                call('/api/article/373.xml'),
                call('/api/article/article_14_2.json'),
                call('/api/article/article_14_2.xml'),
                call('/api/article/374.json'),
                call('/api/article/374.xml'),
                call('/api/article/article_14_3.json'),
                call('/api/article/article_14_3.xml'),
                call('/api/article/375.json'),
                call('/api/article/375.xml')
            ])


class CcIconTest(CcCase):
    """
    изменим икону.
    Должен подчистится кэш у события и у календаря
    """
    @staticmethod
    def get_cleaned_data():
        return {
            'title': 'title',
            'content': 'content',
            'annonce': 'annonce',
        }

    def test_icon_update(self):
        cleaned_data = self.get_cleaned_data()
        icon = MfCalendarIcon.objects.get(pk=361)
        with patch(
            "api.cc._remove_cach_file_by_url", return_value=1
        ) as mock_cc:
            sabnac.update_icon(icon, cleaned_data)
            self.assertEquals(mock_cc.mock_calls, [
                call('/api/event/14.json'),
                call('/api/event/14.xml'),
                call('/api/event/blagoveshenie_presvyatoy_bogorodicy.json'),
                call('/api/event/blagoveshenie_presvyatoy_bogorodicy.xml'),
                call('/api/calendar/2010-04-07.json'),
                call('/api/calendar/2010-04-07.xml'),
                call('/api/calendar/2011-04-07.json'),
                call('/api/calendar/2011-04-07.xml'),
            ])


