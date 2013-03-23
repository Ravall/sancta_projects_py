# -*- coding: utf-8 -*-
import logging
from django import forms
from django.contrib import admin
from smart_date.smartfunction import FormulaException, formula_factory
from smart_date import date
from hell import sabnac
from mf_system import widget
from mf_admin.object import ObjectAdmin, ObjectForm, StatusObjectFilter,\
    TagObjectFilter
from mf_calendar import models as calendar_model
from mf_system.models.mf_article import MfSystemArticle
from mf_system.models.mf_text import MfSystemText
from mf_system.models.mf_object_text import MfSystemObjectText
from mf_system.models.mf_relation import MfSystemRelation


class EventAdminForm(ObjectForm):
    # для икон. заголовок иконы и сама икона
    icon_file = forms.ImageField(required=False)
    icon_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'title'}),
        help_text=u"Название иконы",
    )
    alt_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'text'}),
        help_text=u"пропишется в alt картинки",
    )
    smart_function = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'text'}),
        help_text=u"умная фунция им Алексея Клименко",
    )
    image_file = forms.ImageField(required=False)
    add_article = forms.ChoiceField(required=False)

    def clean_smart_function(self):
        '''
        валидация умной фунции
        '''
        try:
            # возмем эту фунцию за текущий год
            formula_obj = formula_factory(
                self.cleaned_data['smart_function'],
                date.get_current_year(),
            )
            formula_obj.generatelist()
        except FormulaException as exception:
            raise forms.ValidationError(
                'фунция не валидна: {0}'.format(exception)
            )
        return self.cleaned_data["smart_function"]

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        self.set_initial(instance)
        self.initial['icon_title'] = u'Икона ' + self.initial['title']
        self.initial['alt_text'] = self.initial['annonce'].replace("\n", ' ')
        self.initial['smart_function'] = instance.smart_function
        self.fields['add_article'].choices = \
            MfSystemArticle.get_unrelated_articles_select()

    class Meta:
        # указываем что эта таблица расширяет EventAdminForm
        model = calendar_model.MfCalendarEvent


class ObjectTextInline(admin.TabularInline):
    readonly_fields = 'system_object', 'system_text', 'status'
    model = calendar_model.MfCalendarEvent.texts.through
    extra = 0


class EventRelatedInline(admin.TabularInline):
    fields = 'mf_object',
    model = calendar_model.MfCalendarEvent.related_objects.through
    fk_name = "parent_object"
    extra = 0

    def queryset(self, request):
        qs = super(EventRelatedInline, self).queryset(request)
        return qs.filter(mf_object__status="active")


class RelatedObjectsInlineArticle(EventRelatedInline):
    verbose_name_plural = 'Статьи по теме'

    def formfield_for_dbfield(self, db_field, **kwargs):
        '''
        переопределим отображение некоторых полей в инлайн-форме:
        id сделаем ссылкой
        '''
        if db_field.name == 'mf_object':
            kwargs['widget'] = widget.ArticleLinkWidget()
        return super(RelatedObjectsInlineArticle, self).formfield_for_dbfield(
            db_field, **kwargs
        )

    def has_add_permission(self, request):
        return False

    def queryset(self, request):
        qs = super(RelatedObjectsInlineArticle, self).queryset(request)
        return qs.filter(relation=1)


class RelatedObjectsInlineIcons(EventRelatedInline):
    verbose_name_plural = 'Иконы привязанные к событию'
    #readonly_fields = 'mf_object',
    #formset = XXX
    #template = 'admin/object_icons.html'

    def formfield_for_dbfield(self, db_field, **kwargs):
        '''
        переопределим отображение некоторых полей в инлайн-форме икон
        '''
        if db_field.name == 'mf_object':
            kwargs['widget'] = widget.IconWidget()
        return super(RelatedObjectsInlineIcons, self).formfield_for_dbfield(
            db_field, **kwargs
        )

    def queryset(self, request):
        '''
        среди всех связанных объектов нужно выыести только те,
        у которых relation=2 (икона)
        '''
        qs = super(RelatedObjectsInlineIcons, self).queryset(request)
        return qs.filter(relation=2)

    def has_add_permission(self, request):
        '''
        так как иконы добавляются в форме самого события,
        отдельно выводить кнопку "добавить" не нужно
        '''
        return False


class MfCalendarEventAdmin(ObjectAdmin):
    list_display = 'id', 'get_title', 'count_icons', 'count_articles'

    def __init__(self, *args, **kwargs):
        super(MfCalendarEventAdmin, self).__init__(*args, **kwargs)

    def count_icons(self, obj):
        return obj.count_icons

    def count_articles(self, obj):
        return obj.count_articles

    inlines = [
        ObjectTextInline,
        RelatedObjectsInlineArticle,
        RelatedObjectsInlineIcons
    ]
    fieldsets = (
        (None, {
            'fields': ('title', 'smart_function', 'periodic', 'image_file')
        }),
        ('Контент', {
            'classes': ('collapse',),
            'fields': ('annonce', 'content', 'add_article')
        }),
        ('Настройки', {
            'classes': ('collapse',),
            'fields': ('status', 'created', 'updated', 'created_class', 'tags')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('seo_url',)
        }),
        ('Икона', {
            'classes': ('collapse',),
            'fields': ('icon_title', 'alt_text', 'icon_file')
        }),
    )
    list_filter = StatusObjectFilter, TagObjectFilter
    form = EventAdminForm
    change_form_template = 'admin/imaged_object_change_form.html'

    def save_icon(self, request, obj, form, change):
        if len(request.FILES) == 0:
            return None
        # создаем объект икона
        icon = calendar_model.MfCalendarIcon(
            status='active',
            created_class='MfCalendarIcon'
        )
        icon.save()
        icon.load_file(
            request.FILES['icon_file'],
            form.cleaned_data['icon_title']
        )
        # создаем текст
        icon.create_text(form.cleaned_data)
        obj.add_icon(icon)

    def add_article(self, request, obj, form, change):
        """
        привязываем статью
        """
        article_id = form.cleaned_data['add_article']
        if article_id:
            relation = MfSystemRelation(
                relation_id=1,
                parent_object=obj,
                mf_object_id=form.cleaned_data['add_article']
            )
            relation.save()

    def save_model(self, request, obj, form, change):
        # чистка кэша
        sabnac.update_event.delay(obj, form.cleaned_data)

        super(MfCalendarEventAdmin, self).save_model(
            request, obj, form, change
        )
        # загруженный файл
        #file_data = dict(
        #    image_file = request.FILES['image_file'],
        #    image_title = form.cleaned_data.get('title')
        #) if len (request.FILES) != 0 else None

        #привяжем статью
        self.add_article(request, obj, form, change)

        self.save_text(request, obj, form, change)
        self.save_icon(request, obj, form, change)
        self.save_seo(request, obj, form, change)


