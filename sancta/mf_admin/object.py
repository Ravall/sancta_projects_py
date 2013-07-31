# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from mf_system import models as system_model
from mf_calendar import models as calendar_model
from mf_system import widget
from taggit.models import Tag, TaggedItem
from mf_system.models.mf_object_text import MfSystemObjectText
from mf_admin.widgets import ObjectLinkWidget, MyTinyMCE


class ObjectForm(forms.ModelForm):
    # pylint: disable=R0924
    '''
    общий класс для дополнительных форм, модели которых отнаследованы от object
    '''
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title'}))
    seo_url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'text'}),
        required=False
    )
    annonce = forms.CharField(widget=forms.Textarea, required=False)
    #content = forms.CharField(widget=forms.Textarea, required=False)
    content = forms.CharField(
        widget=MyTinyMCE.Widget(
            attrs={'cols': 800, 'rows': 30},
        ),
        required=False
    )
    image = forms.ImageField(widget=widget.ImageWidget, required=False)
    exclude = 'created_class',

    def set_initial(self, instance):
        if instance is not None:
            text = MfSystemObjectText.objects.get(
                system_object_id=instance.id,
                status=u'Active'
            ).system_text
            self.initial['title'] = text.title
            self.initial['annonce'] = text.annonce
            self.initial['content'] = text.content
            self.initial['seo_url'] = instance.url


class RelatedInlineObject(admin.TabularInline):
    '''
    когда редактируем объект, нужно вывести все объекты, к которым
    он привязан.
    Эта инлайн-форма подключена по-умолчанию
    '''
    fields = 'parent_object',
    fk_name = "mf_object"
    verbose_name_plural = 'Принадлежность к объектам:'
    model = calendar_model.MfCalendarEvent.related_objects.through
    extra = 0

    def queryset(self, request):
        # pylint: disable=E1002
        query_set = super(RelatedInlineObject, self).queryset(request)
        return query_set.filter(mf_object__status="active")

    def formfield_for_dbfield(self, db_field, **kwargs):
        # pylint: disable=E1002
        """
        переопределим отображение некоторых полей в инлайн-форме:
        id сделаем ссылкой
        """
        if db_field.name == 'parent_object':
            kwargs['widget'] = ObjectLinkWidget
        return super(RelatedInlineObject, self).formfield_for_dbfield(
            db_field, **kwargs
        )

    def has_add_permission(self, request):
        # pylint: disable=E1002
        """
        так как иконы добавляются в форме самого события,
        отдельно выводить кнопку "добавить" не нужно
        """
        super(RelatedInlineObject, self).has_add_permission(request)
        return False


class ObjectAdmin(admin.ModelAdmin):
    '''
    общее для admin.ModelAdmin для моделей, основанных на object
    '''
    list_display = 'id', 'get_title'
    readonly_fields = 'created', 'updated', 'created_class'
    inlines = RelatedInlineObject,

    @staticmethod
    def save_text(request, obj, form, change):
        # pylint: disable=W0613
        if change:
            # если изменяется объект
            text = MfSystemObjectText.objects.get(
                system_object_id=obj.id,
                status=u'Active'
            ).system_text
            text.title = form.cleaned_data['title']
            text.annonce = form.cleaned_data['annonce']
            text.content = form.cleaned_data['content']
            text.save()
        else:
            # если создается новый объект
            # создаем текст
            obj.create_text(dict(
                title=form.cleaned_data['title'],
                annonce=form.cleaned_data['annonce'],
                content=form.cleaned_data['content']
            ))

    @staticmethod
    def save_seo(request, obj, form, change):
        # pylint: disable=W0613
        obj.save_seo_url(form.cleaned_data)

    def delete_model(self, request, obj):
        '''
        в формах унаследованных от ObjectAdmin (объект системный),
        удаление модели - приводит к изменению статуса объекта
        '''
        system_model.MfSystemObject\
            .objects.filter(pk=obj.id).update(status='deleted')

    def get_title(self, object):
        # pylint: disable=W0622,R0201
        return object.title

    class Media:
        # pylint: disable=W0232
        css = {
            "all": ("css/b_forms.css", "css/edit_form.css")
        }


class StatusObjectFilter(admin.SimpleListFilter):
    '''
    фильтр для всех форм, унаследованных от ObjectAdmin
    фильтрут по статусу - активные и все остальные :)
    '''
    title = u'статус'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            (None, u'активные'),
            ('off', u'Удаленные и на паузе'),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter(status__in=['active', ])
        if self.value() == 'off':
            return queryset.filter(status__in=['deleted', 'pause'])

    def choices(self, chs):
        '''
        переопределил метод, который возвращает список пунктов меню фильтра
        и убрал от туда первый 'все'
        '''
        return list(super(StatusObjectFilter, self).choices(chs))[1:]


class IsObjectRelateFilter(admin.SimpleListFilter):
    """
    фильтр привязнности. Находит непривязанные объекты
    """
    title = u'привязанность'
    parameter_name = 'is_related'

    def lookups(self, request, model_admin):
        return (
            ('off', u'непривязанные'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'off':
            """
            для каждой статьи делаем запрос - узнаем сколько объектов
            ее привязали к себе
            """
            return queryset.extra(
                where=[
                    '(SELECT count(*) FROM mf_system_relation srlt WHERE '
                    '`srlt`.`mf_object_id` = `mf_system_object`.`id`) = 0'
                ],
            )


class TagObjectFilter(admin.SimpleListFilter):
    title = u'теги'
    parameter_name = 'tag'

    def queryset(self, request, queryset):
        if self.value() is not None:
            """
            для каждой статьи делаем запрос - узнаем сколько объектов
            ее привязали к себе
            """
            return queryset.filter(tags__name__in=[self.value()])

    def lookups(self, request, model_admin):
        # фильтр привязан к админКлассу. который связан с моделью
        # нужно из модели получить имя модели
        # не знаю способ кроме такого:
        # str(model_admin.opts.concrete_model._meta).split('.')[-1]
        # обращаюсь к мета - это плохо
        # pylint: disable=W0212
        tmp = set()
        ids = [
            tagitem.tag_id
            for tagitem in TaggedItem.objects.filter(
                content_type__model=str(
                    model_admin.opts.concrete_model._meta
                ).split('.')[-1]
            ) if tagitem.tag_id not in tmp and not tmp.add(tagitem.tag_id)
        ]
        return [
            (tag.name,) * 2
            for tag in Tag.objects.filter(pk__in=ids)
        ]
