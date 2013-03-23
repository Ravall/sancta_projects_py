# -*- coding: utf-8 -*-
"""
Тестирование API
- проверить получение иконы, события удаленного (или на паузе)
- проверить получение события и икон его, при наличии статей и удаленных икон
"""
# pylint: disable=E1103
import ast
from django.test import TestCase, Client
from mf_system.models import MfSystemArticle
from mf_calendar.models import MfCalendarEvent


class ApiTest(TestCase):
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


class SmokTest(ApiTest):
    def test_show_info_get(self):
        api_client = Client()
        response = api_client.get('/api.json')
        self.assertEquals(response.status_code, 200)
        # ответ получим в виде строки в которой dict
        # преобразуем строку в dict
        content = ast.literal_eval(response.content)
        self.assertTrue(content.get('example', False))


class ArticleTest(ApiTest):
    def test_get_article(self):
        def assert_article373(article):
            self.assertEquals(article['id'], 373)
            self.assertEquals(article['type'], 'article')
            self.assertEquals(article['image'], 'img_article_14_1.jpg')
            self.assertEquals(article['name'], 'article_14_1')
            self.assertEquals(article['text']['title'], 'article 14 1 tilte')
            self.assertEquals(
                article['text']['annonce'], 'article 14 1 annonce'
            )
            self.assertEquals(
                article['text']['content'], 'article 14 1 content'
            )

        api_client = Client()
        response = api_client.get(
            '/api/article/{0}.{1}'.format(373, 'json')
        )
        self.assertEquals(response.status_code, 200)
        content = ast.literal_eval(response.content)
        assert_article373(content)
        response = api_client.get(
            '/api/article/{0}.{1}'.format('article_14_1', 'json')
        )
        self.assertEquals(response.status_code, 200)
        content = ast.literal_eval(response.content)
        assert_article373(content)
        self.assertEquals(content['related'][0]['type'], 'event')
        self.assertEquals(content['related'][0]['id'], 14)
        self.assertFalse('tags' in content)

    def test_get_article_by_tag(self):
        """
        проверим получение статей по тегам
        """
        api_client = Client()
        response = api_client.get(
            '/api/article/tag/{0}.{1}'.format('xxx', 'json')
        )
        self.assertEquals(response.status_code, 404)

        article = MfSystemArticle.objects.get(pk=373)
        article.tags.add('tag1', 'tag2')
        article = MfSystemArticle.objects.get(pk=374)
        article.tags.add('tag2', 'tag3')
        article = MfSystemArticle.objects.get(pk=375)
        article.tags.add('tag1', 'tag3')
        response = api_client.get(
            '/api/article/{0}.{1}'.format(374, 'json')
        )
        content = ast.literal_eval(response.content)
        self.assertTrue('tags' in content)
        self.assertEquals(['tag2', 'tag3'], content['tags'])

        response = api_client.get(
            '/api/article/tag/{0}.{1}'.format('tag1', 'json')
        )
        content = ast.literal_eval(response.content)
        self.assertEquals(2, len(content))
        self.assertEquals(373, content[0]['id'])
        self.assertEquals(375, content[1]['id'])

    def test_get_aricles_by_event(self):
        api_client = Client()
        response = api_client.get(
            '/api/event/{0}.{1}'.format(14, 'json')
        )
        self.assertEquals(response.status_code, 200)
        content = ast.literal_eval(response.content)
        self.assertEquals(3, len(content['articles']))
        self.assertEquals(373, content['articles'][0]['id'])
        self.assertEquals(374, content['articles'][1]['id'])
        self.assertEquals(375, content['articles'][2]['id'])


class EventTest(ApiTest):

    def test_get_event(self):
        """
        Тестируем получение через api события
        по id и по url
        """
        def assert_krestopoklonnaya(content):
            self.assertEquals(
                content['text']['title'], 'nedelya_krestopoklonnaya tilte'
            )
            self.assertEquals(
                content['text']['annonce'], 'nedelya_krestopoklonnaya annonce'
            )
            self.assertEquals(
                content['text']['content'], 'nedelya_krestopoklonnaya content'
            )
            self.assertEquals(
                content['id'], 50
            )
            self.assertEquals(
                content['image'], '1321823855_410.jpg'
            )
            self.assertEquals(
                content['name'], 'nedelya_krestopoklonnaya'
            )
        api_client = Client()
        # когда события не существует
        response = api_client.get(
            '/api/event/{0}.{1}'.format(100, 'json')
        )
        self.assertEquals(response.status_code, 404)
        response = api_client.get(
            '/api/event/{0}.{1}'.format(50, 'json')
        )
        self.assertEquals(response.status_code, 200)
        content = ast.literal_eval(response.content)
        assert_krestopoklonnaya(content)
        response = api_client.get(
            '/api/event/{0}.{1}'.format('nedelya_krestopoklonnaya', 'json')
        )
        self.assertEquals(response.status_code, 200)
        content = ast.literal_eval(response.content)
        assert_krestopoklonnaya(content)
        response = api_client.get(
            '/api/event/{0}.{1}'.format('tr_test_title_fix', 'json')
        )
        self.assertEquals(response.status_code, 404)

    def test_get_unactive_event(self):
        '''
        события с id=99 не активно (из фикстур)
        '''
        api_client = Client()
        response = api_client.get(
            '/api/event/{0}.{1}'.format(99, 'json')
        )
        self.assertEquals(response.status_code, 404)

    def test_get_event_by_tag(self):
        event = MfCalendarEvent.objects.get(pk=14)
        event.tags.add('tag1', 'tag2')
        event = MfCalendarEvent.objects.get(pk=50)
        event.tags.add('tag2', 'tag3')
        event = MfCalendarEvent.objects.get(pk=27)
        event.tags.add('tag1', 'tag3')
        api_client = Client()
        response = api_client.get(
            '/api/event/tag/{0}.{1}'.format('tag1', 'json')
        )
        content = ast.literal_eval(response.content)
        self.assertEquals(2, len(content))
        self.assertEquals(14, content[0]['id'])
        self.assertEquals(27, content[1]['id'])


class IconsTest(ApiTest):
    """
    тестируем получение икон
    """
    def test_show_icnos_info(self):
        api_client = Client()
        response = api_client.get(
            '/api/event/{0}.{1}'.format(14, 'json')
        )
        content = ast.literal_eval(response.content)
        self.assertEquals(2, len(content['icons']))
        #проверить все поля
        self.assertEquals(
            content['icons'][0]['type'], 'icon'
        )
        self.assertEquals(
            content['icons'][0]['id'], 369
        )
        self.assertEquals(
            content['icons'][0]['text']['title'], 'icon 2 tilte'
        )
        self.assertEquals(
            content['icons'][0]['text']['annonce'], 'icon 2 annonce'
        )
        self.assertEquals(
            content['icons'][0]['text']['content'], 'icon 2 content'
        )
        self.assertEquals(
            content['icons'][0]['image'],
            'ikona-blagoveshenie-presvyatoy-bogorodicy.jpg'
        )
        self.assertEquals(
            content['icons'][1]['id'], 371
        )
        self.assertEquals(
            content['icons'][1]['text']['title'], 'icon 4 tilte'
        )
        self.assertEquals(
            content['icons'][1]['text']['annonce'], 'icon 4 annonce'
        )
        self.assertEquals(
            content['icons'][1]['text']['content'], 'icon 4 content'
        )
        self.assertEquals(
            content['icons'][1]['image'],
            'ikona-blagoveshenie-presvyatoy-bogorodicy1.jpg'
        )
        self.assertFalse('related' in content['icons'][0])
        self.assertFalse('related' in content['icons'][1])


class CalendarTest(ApiTest):
    def test_get_empty_date(self):
        api_client = Client()
        response = api_client.get(
            '/api/calendar/{0}.{1}'.format('4023-12-01', 'json')
        )
        self.assertEquals(response.status_code, 200)

    def test_get_incorrect_date(self):
        api_client = Client()
        response = api_client.get(
            '/api/calendar/{0}.{1}'.format('2013-99-99', 'json')
        )
        self.assertEquals(response.status_code, 404)

    def test_get_by_date(self):
        """
        тестируем получение инорфмации по дню календаря
        """
        api_client = Client()
        response = api_client.get(
            '/api/calendar/{0}.{1}'.format('2013-04-07', 'json')
        )
        self.assertEquals(response.status_code, 200)
        content = ast.literal_eval(response.content)
        self.assertEquals('2013-04-07', content['date'])
        self.assertEquals(3, len(content['events']))

        self.assertFalse(content['events'][0].get('icons', False))

        self.assertEquals(
            'ikona-blagoveshenie-presvyatoy-bogorodicy.jpg',
            content['events'][1]['icons'][0]['image']
        )
        self.assertEquals(
            14, content['events'][1]['id']
        )
        self.assertEquals(
            'icon', content['events'][1]['icons'][0]['type']
        )
        self.assertEquals(
            369, content['events'][1]['icons'][0]['id']
        )
        self.assertEquals(
            'icon 2 tilte', content['events'][1]['icons'][0]['text']['title']
        )
        self.assertEquals(
            'icon', content['events'][1]['icons'][1]['type']
        )
        self.assertEquals(
            371, content['events'][1]['icons'][1]['id']
        )
        self.assertEquals(
            50, content['events'][2]['id']
        )
        self.assertEquals(
            'icon', content['events'][2]['icons'][0]['type']
        )
        self.assertEquals(
            372, content['events'][2]['icons'][0]['id']
        )
