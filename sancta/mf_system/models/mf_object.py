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
from taggit_autocomplete_modified.managers \
    import TaggableManagerAutocomplete as TaggableManager
from ordered_model.models import OrderedModel
from urlparse import urlparse, parse_qs

class MfSystemObject(OrderedModel):
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
    site = models.ForeignKey(Site, default=1)
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


    def save_seo_url(self, params, **kargs):
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

    @transaction.commit_manually
    def create_text(self, text_content, status='active'):
        """
        создает текст и привязывает его к объекту
        text_content - словарь
            {'title':'', annonce:'',content:''}
        status - черновик, чистовик

        """
        try:
            # сохраняем сам текст
            text = MfSystemText(
                title=text_content.get('title', ''),
                annonce=text_content.get('annonce', ''),
                content=text_content.get('content', ''),
                keywords=text_content.get('keywords', '')
            )
            text.save()
            # привязываем текст к объекту
            self._relate_with_text(text, status)
        except Exception, e:
            transaction.rollback()
            text.delete()
            raise e
        else:
            transaction.commit()

    def update_text(self, text_content, status='active'):
        self.texts.filter(mfsystemobjecttext__status=status).update(
            title=text_content.get('title', ''),
            annonce=text_content.get('annonce', ''),
            keywords=text_content.get('keywords', ''),
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
        return [
            self.factory(related.parent_object) for related in relateds
        ]

    @staticmethod
    def factory(obj):
        if obj.created_class == 'MfCalendarEvent':
            from mf_calendar.models import MfCalendarEvent
            factory_obj = MfCalendarEvent.objects.get(pk=obj.id)
        elif obj.created_class == 'MfSystemArticle':
            from mf_system.models import MfSystemArticle
            factory_obj = MfSystemArticle.objects.get(pk=obj.id)
        elif obj.created_class == 'MfCalendarIcon':
            from mf_system.models import MfCalendarIcon
            factory_obj = MfCalendarIcon.objects.get(pk=obj.id)
        return factory_obj

    def _move(self, up, request):
        """
        Переопределяем фунцию _move для модуля django-ordered-model
        Добавляем учет тегов:
          если список статей выдан с фильтром по тегу - то фильтруем с учетом тега
        """
        params = {}
        try:
            get_params =  parse_qs(
                urlparse(
                    request.META['HTTP_REFERER']
                ).query
            )
            if 'tag' in get_params:
                # фильтр идет по одному тегу обычно
                params['tags__name__in'] = get_params['tag']
            if 'site__id__exact' in get_params:
                params['site'] = get_params['site__id__exact'][0]
        except Exception:
            pass

        qs = self.__class__._default_manager
        if up:
            params['order__lt'] = self.order
            qs = qs.order_by('-order').filter(**params)
        else:
            params['order__gt'] = self.order
            qs = qs.filter(**params)
        try:
            replacement = qs[0]
        except IndexError:
            # already first/last
            return
        self.order, replacement.order = replacement.order, self.order
        self.save()
        replacement.save()
        from hell import sabnac
        sabnac.update_article.delay(self)
        sabnac.update_article.delay(replacement)

    def move_down(self, request):
        """
        Move this object down one position.
        """
        return self._move(False, request)

    def move_up(self, request):
        """
        Move this object up one position.
        """
        return self._move(True, request)


    class Meta:
        db_table = u'mf_system_object'
        managed = False
        app_label = 'sancta'
        ordering = ('order',)


# south не пропускает кастомные поля
from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^taggit_autocomplete_modified\.managers"])
