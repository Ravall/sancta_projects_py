# -*- coding: utf-8 -*-
"""
модель объект. Общая часть для многих моделей
"""
from django.db import models, transaction
from .mf_text import MfSystemText
from .mf_object_text import MfSystemObjectText
from .mf_relation import MfSystemRelation
from tools import load_file
from tools.grammar import translite
from django.contrib.sites.models import Site
from taggit.managers import TaggableManager


class MfSystemObject(models.Model):
    status = models.CharField(
        max_length=21,
        choices=(
            ('active', 'Активный'),
            ('pause', 'На паузе'),
            ('deleted', 'Удален')
        ),
        default='active'
    )
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField()
    created_class = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='origin/')
    texts = models.ManyToManyField(MfSystemText, through='MfSystemObjectText')
    # для seo - транслитирированный url
    url = models.CharField(max_length=250, blank=True, null=True)
    related_objects = models.ManyToManyField(
        "self", through=MfSystemRelation,
        symmetrical=False, related_name='related'
    )
    site = models.ForeignKey(Site)
    tags = TaggableManager(blank=True)

    def get_title(self):
        return self.texts.filter(
            mfsystemobjecttext__status='active'
        ).get().title

    def get_annonce(self):
        return self.texts.filter(
            mfsystemobjecttext__status='active'
        ).get().annonce

    def get_content(self):
        return self.texts.filter(
            mfsystemobjecttext__status='active'
        ).get().content

    def __unicode__(self):
        return "%s" % self.id

    def load_file(self, image_file, filename):
        file_name = load_file.handle_uploaded_file(
            image_file,
            filename
        )
        self.image = file_name
        self.save()

    def _relate_with_text(self, text, status):
        """
        привязывает к объекту текст
        """
        system_object_text = MfSystemObjectText(
            status=status,
            system_object=self,
            system_text=text
        )
        system_object_text.save()
        return system_object_text

    def _save_seo_url(self, params, **kargs):
        """
        сохраняет seo_url из словаря params
        params = {'seo_url':'', 'title':"}
        транслитирируем полученное значение
        """
        url = params.get('seo_url')
        if not url:
            url = params.get('title')
        self.url = translite(url)
        if not kargs.get('commit', False):
            self.save()

    @transaction.commit_on_success
    def create_text(self, text_content, status='active'):
        """
        создает текст и привязывает его к объекту
        text_content - словарь
            {'title':'', annonce:'',content:''}
        status - черновик, чистовик

        """
        # сохраняем сам текст
        text = MfSystemText(
            title=text_content.get('title', ''),
            annonce=text_content.get('annonce', ''),
            content=text_content.get('content', ''),
        )
        text.save()
        # привязываем текст к объекту
        self._relate_with_text(text, status)

    def update_text(self, text_content, status='active'):
        self.texts.filter(mfsystemobjecttext__status=status).update(
            title=text_content.get('title', ''),
            annonce=text_content.get('annonce', ''),
            content=text_content.get('content', '')
        )

    def is_related(self):
        """
        проверяет привязан ли объект к чему либо
        """
        return MfSystemRelation.objects.filter(mf_object=self).count()

    def get_relate_to(self):
        """
        получаем все объекты, к которому привязан текущий объект
        """
        relateds = MfSystemRelation.objects.filter(mf_object=self)
        return [related.parent_object for related in relateds]


    class Meta:
        db_table = u'mf_system_object'
        managed = False
        app_label = 'sancta'
