# -*- coding: utf-8 -*-
from django.db import transaction
from .mf_object import MfSystemObject
from .object_manager import SystemObjectManager
from tools import load_file


class MfSystemArticleException(Exception):
    pass


# статьи
class MfSystemArticle(MfSystemObject):
    objects = SystemObjectManager('mf_system_article.mfsystemobject_ptr_id')

    class Meta:
        db_table = u'mf_system_article'
        managed = False
        app_label = 'sancta'
        verbose_name = 'article'
        verbose_name_plural = 'Статьи'

    @staticmethod
    def get_unrelated_extra():
        return dict(where=[
            '(SELECT count(*) FROM mf_system_relation srlt WHERE '
            ' `srlt`.`mf_object_id` = `mf_system_object`.`id`) = 0'
            ],
        )

    @classmethod
    def get_unrelated_articles_select(cls):
        """
        получить статьи непривязанные к объектам
        # добавить статус актив и вывести текст
        # без привязки к тегам
        """
        return [('', '---------')] + [
            (art.id, art.title) for art in
            # привязать можно только активные
            cls.objects.filter(
                status__in=['active'],
            # и без тегов
            ).exclude(
                tags__in=cls.tags.all()
            ).extra(**cls.get_unrelated_extra())
        ]

    @transaction.commit_manually
    def update(self, params, up_file=False):
        try:
            filename, old_filename = None, str(self.image)
            self.save_seo_url(params)
            self.update_text(params)
            if up_file:
                filename = self.load_file(
                    up_file['image_file'],
                    up_file['image_title']
                )
        except Exception, ext:
            transaction.rollback()
            # если успели загрузить файл и откатываем по ошибке,
            # то файл можно убить
            if filename:
                load_file.delete_file(filename)
            #прокидываем ошибку дальше
            raise MfSystemArticleException(
                'ошибка при обновлении статьи {0}'.format(ext)
            )
        else:
            # если все хорошо
            transaction.commit()
            #удаляем старый файл
            if up_file and old_filename:
                load_file.delete_file(old_filename)

    @transaction.commit_manually
    def create(self, params, up_file=False):
        """
        досоздать статью.
        создается тексты, грузится файл, устанавливаются правильные параметры
        все это на основе существования self
        все транзакционно - при возникновении ошибки, откатывается
        """
        try:
            filename = None
            self.save_seo_url(params, commit=False)
            self.created_class = 'MfSystemArticle'
            self.save()
            if up_file:
                filename = self.load_file(
                    up_file['image_file'],
                    up_file['image_title']
                )
            self.create_text(params)
        except Exception, ext:
            transaction.rollback()
            # если успели загрузить файл и откатываем по ошибке,
            # то файл можно убить
            if filename is not None:
                load_file.delete_file(filename)
            #прокидываем ошибку дальше
            raise MfSystemArticleException(
                'ошибка при создании статьи. {0}'.format(ext)
            )
        else:
            transaction.commit()
        return self
