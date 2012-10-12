# -*- coding: utf-8 -*-
import uuid
import os

from django import forms
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe

from mf_system import models as system_model
from mf_calendar import models as calendar_model


def handle_uploaded_file(request_file):
    '''
    загружаем файл из request, сохраняем с уникальным именем
    очищаем exif данные
    '''
    def upload_file(request_file, new_filename):
        '''
        берем из request файл и грузим его в нужную папку
        '''
        destination = open(settings.ORIGIN_MEDIA_ROOT+'/'+new_filename, 'wb+')
        for chunk in request_file.chunks():
            destination.write(chunk)
        destination.close()

    # разделяем имя файла и его расширение
    file_name_info = os.path.splitext(request_file.name)
    # генерируем уникальное имя файла
    new_filename = str(uuid.uuid4())+file_name_info[1]
    # загружаем файл
    upload_file(request_file, new_filename)
    ## удаляем мета теги и перемещаем в новую папку
    os.system('exiftool -all= ' + new_filename)
    return new_filename


class MfSystemRelationTypeAdmin(admin.ModelAdmin):
    list_display = ('id','relation_name')

class ObjectTextInline(admin.TabularInline):
    readonly_fields = ('system_object', 'system_text', 'status')
    model = calendar_model.MfCalendarEvent.texts.through
    extra = 0


class EventRelatedInline(admin.TabularInline):
    fields = ('mf_object',)
    model = calendar_model.MfCalendarEvent.related_objects.through
    fk_name = "parent_object"
    extra = 0





class RelatedObjectsInlineArticle(EventRelatedInline):
    verbose_name_plural = 'Статьи по теме'

    def queryset(self, request):
        qs = super(RelatedObjectsInlineArticle, self).queryset(request)
        return qs.filter(relation=1)


class IconWidget(forms.Widget):
    '''
    виджет изображения привязанной иконы
    замяет текущую форму на hidden поле и добавляет ссылку на изображение
    '''
    def render(self, name, value, attrs=None):
        if not value:
            return ''
        hidden = forms.HiddenInput(attrs)
        icon = calendar_model.MfCalendarIcon.objects.get(pk=value)
        return mark_safe('<img width=100px src="/media/origin/%s">' % icon.image)+hidden.render(name, value)

class RelatedObjectsInlineIcons(EventRelatedInline):
    verbose_name_plural = 'Иконы привязанные к событию'

    def formfield_for_dbfield(self, db_field, **kwargs):
        '''
        переопределим отображение некоторых полей в инлайн-форме икон
        '''
        if db_field.name == 'mf_object':

            kwargs['widget'] = IconWidget()
        field = super(RelatedObjectsInlineIcons, self).formfield_for_dbfield(db_field, **kwargs)
        return field

    def queryset(self, request):
        qs = super(RelatedObjectsInlineIcons, self).queryset(request)
        return qs.filter(relation=2)




class TextAdmin(admin.ModelAdmin):
	inlines = [
        ObjectTextInline
    ]


class IconAdmin(admin.ModelAdmin):
	readonly_fields = ('created', 'updated')
	pass



class EventAdminForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'title'}))
    annonce = forms.CharField(widget=forms.Textarea, required=False)
    content = forms.CharField(widget=forms.Textarea)
    exclude=('created_class',)

    # для икон. заголовок иконы и сама икона
    icon_file = forms.ImageField(required=False)
    icon_title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'title'}), help_text=u"Название иконы")
    alt_text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'text'}), help_text=u"пропишется в alt картинки")

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        text = system_model.MfSystemObjectText.objects.get(system_object_id=instance.id,status=u'Active').system_text
        self.initial['title'] = text.title
        self.initial['annonce'] = text.annonce
        self.initial['content'] = text.content
        self.initial['icon_title'] = u'Икона '+text.title
        self.initial['alt_text'] = text.annonce

    class Meta:
    	# указываем что эта таблица расширяет EventAdminForm
    	model = calendar_model.MfCalendarEvent


class MfCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    readonly_fields = ('created', 'updated','created_class', 'function')
    inlines = [
        ObjectTextInline, RelatedObjectsInlineArticle, RelatedObjectsInlineIcons
    ]
 	#exclude=('related_objects',)

    fieldsets=(
    	(None, {'fields':('title', 'function', 'periodic')}),
    	('Контент', {'classes': ('collapse',),'fields':('annonce','content')}),
    	('Настройки', {'classes': ('collapse',),'fields':('status', 'created','updated','created_class')}),
    	('Икона', {'classes': ('collapse',),'fields':('icon_title', 'alt_text', 'icon_file')}),

    )
    class Media:
        css = {
            "all": ("css/b_forms.css",)
        }

    form = EventAdminForm


    def save_text(self, request, obj, form, change):
    	text = system_model.MfSystemObjectText.objects.get(system_object_id=obj.id,status=u'Active').system_text
    	text.title = form.cleaned_data['title']
    	text.save()

    def save_icon(self, request, obj, form, change):
        if len(request.FILES) == 0:
            return None
        #сохраняем файл
        file_name = handle_uploaded_file(request.FILES['icon_file'])
        # создаем объект икона
        icon = calendar_model.MfCalendarIcon(status='active', image=file_name, created_class='MfCalendarIcon')
        icon.save()
        # создаем текст
        icon_text = system_model.MfSystemText(title=form.cleaned_data['icon_title'],annonce=form.cleaned_data['alt_text'])
        icon_text.save()
        # привязываем текст к объекту
        system_object_text = system_model.MfSystemObjectText(status='active', system_object=icon, system_text=icon_text)
        system_object_text.save()
        # привязываем икону к редактируемому объекту
        relation = system_model.MfSystemRelation(relation_id=2, parent_object = obj, mf_object=icon)
        relation.save()



    def save_model(self, request, obj, form, change):
    	super(MfCalendarEventAdmin, self).save_model(request, obj, form, change)
    	self.save_text(request, obj, form, change)
    	self.save_icon(request, obj, form, change)




admin.site.register(system_model.MfSystemRelationType, MfSystemRelationTypeAdmin)
admin.site.register(calendar_model.MfCalendarEvent, MfCalendarEventAdmin)
admin.site.register(system_model.MfSystemText, TextAdmin)
admin.site.register(calendar_model.MfCalendarIcon, IconAdmin)
