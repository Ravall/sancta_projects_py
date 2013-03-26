# -*- coding: utf-8 -*-
from django import forms
from mf_admin.object import ObjectAdmin, StatusObjectFilter,\
    ObjectForm, IsObjectRelateFilter, TagObjectFilter
from mf_system.models.mf_article import MfSystemArticle
from hell import sabnac


class ArticleForm(ObjectForm):
    image_file = forms.ImageField(required=False)
    id = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        self.set_initial(instance)

    def clean(self):
        """
        """
        cleaned_data = self.cleaned_data
        if cleaned_data.get('tags', False) and self.instance.is_related():
            # если установлены теги и привязана статья - это не правильно
            raise forms.ValidationError('Нельзя устанавливать теги, к приявзанной статье')
        return cleaned_data

    class Meta:
        # указываем что эта таблица расширяет ArticleForm
        model = MfSystemArticle


class MfSystemArticleAdmin(ObjectAdmin):
    list_display = 'id', 'get_title'
    list_filter = StatusObjectFilter, IsObjectRelateFilter, TagObjectFilter, 'site'
    form = ArticleForm
    change_form_template = 'admin/imaged_object_change_form.html'
    fieldsets = (
        (None, {'fields': ('title', 'content', 'tags', 'image_file')}),
        ('Настройки', {
            'classes': ('collapse',),
            'fields': ('status', 'created', 'updated', 'created_class', 'site')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('seo_url', 'annonce')
        }),
    )

    def save_model(self, request, obj, form, change):
        # чистка кэша
        sabnac.update_article.delay(obj, form.cleaned_data)

        super(MfSystemArticleAdmin, self).save_model(request, obj, form, change)
        file_data = dict(
            image_file=request.FILES['image_file'],
            image_title=form.cleaned_data.get('title')
        ) if len(request.FILES) != 0 else None
        if not change:
            # если объект новый
            obj.create(form.cleaned_data, file_data)
        else:
            obj.update(form.cleaned_data, file_data)