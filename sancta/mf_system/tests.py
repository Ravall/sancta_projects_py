# -*- coding: utf-8 -*-
from django.test import TestCase
from mf_system.models.mf_article import MfSystemArticle, MfSystemArticleException
from mf_system.models.mf_object import MfSystemObject
from mf_system.models.mf_text import MfSystemText
from mock import patch


class ArticleTest(TestCase):
    def _create_article(self, text_params):
        article = MfSystemArticle()
        article.save()
        article.create(text_params)
        return article

    def test_create_simpe(self):
        """
        проверка правильности создания статьи
        """
        article = self._create_article(
            dict(
                title='test_tile',
                annonce='test_annonce',
                content='test_content'
            )
        )
        article_id = article.id
        # проверим что статья создалась
        self.assertTrue(article_id > 0)
        article = MfSystemArticle.objects.get(pk=article_id)
        # проверим контент
        self.assertEquals(article.get_title(), 'test_tile')
        self.assertEquals(article.get_annonce(), 'test_annonce')
        self.assertEquals(article.get_content(), 'test_content')
        # проверим тех. данные
        s_object = MfSystemObject.objects.get(pk=article_id)
        self.assertEquals(s_object.created_class, 'MfSystemArticle')
        #проверим дополнительные параметры
        self.assertEquals(article.url, 'test_tile')

    def test_fail_save(self):
        """
        тест неправильного сохранения
        подменим метод _relate_with_text на ошибочный,
        проверим, как поведет сохранение
        """
        class TestException(Exception):
            pass

        article = MfSystemArticle()
        article.save()
        count_articles = MfSystemArticle.objects.count()
        count_objects = MfSystemObject.objects.count()

        text = MfSystemText(
            title='1',
            annonce='2',
            content='3'
        )
        text.save()
        count_texts = MfSystemText.objects.count()
        with patch.object(
            MfSystemArticle, '_relate_with_text', side_effect=TestException()
        ), patch.object(
            MfSystemArticle, "load_file", return_value='test_file_name'
        ), patch("tools.load_file.delete_file", return_value=1) as mock_file:
            try:
                article.create(
                    dict(
                        title='test_tile2',
                        annonce='test_annonce2',
                        content='test_content2',
                    ),
                    dict(
                        image_file='file',
                        image_title='file_title'
                    )
                )
                is_except = False
            except MfSystemArticleException:
                is_except = True
        # убеждаемся что исклчение было брошено, что мок заменен верно
        self.assertTrue(is_except)
        # проверим что количество объектов не изменилось
        self.assertEquals(MfSystemArticle.objects.count(), count_articles)
        self.assertEquals(MfSystemObject.objects.count(), count_objects)
        self.assertEquals(MfSystemText.objects.count(), count_texts)
        # проверим что файл удалился правильный
        mock_file.assert_called_with('test_file_name')

    def test_update(self):
        article = self._create_article(dict(
            title='test_tile_1',
            annonce='test_annonce_1',
            content='test_content_1',
        ))
        article.update(dict(
            title='test_tile2',
            annonce='test_annonce2',
            content='test_content2',
        ))
        article = MfSystemArticle.objects.get(pk=article.id)
        # проверим контент
        self.assertEquals(article.get_title(), 'test_tile2')
        self.assertEquals(article.get_annonce(), 'test_annonce2')
        self.assertEquals(article.get_content(), 'test_content2')

