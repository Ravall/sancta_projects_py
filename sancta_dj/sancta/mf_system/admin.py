# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.contrib.contenttypes import generic
from mf_system import models as system_model
from mf_calendar import models as calendar_model

from django import forms


class MfSystemRelationTypeAdmin(admin.ModelAdmin):
    list_display = ('id','relation_name')

class ObjectTextInline(admin.TabularInline):
    readonly_fields = ('system_object', 'system_text', 'status')
    model = calendar_model.MfCalendarEvent.texts.through
    extra = 0

class RelatedObjectsInline(admin.TabularInline):
    readonly_fields = ('parent_object', 'mf_object', 'relation')
    model = calendar_model.MfCalendarEvent.related_objects.through
    fk_name = "parent_object"
    extra = 0


class TextAdmin(admin.ModelAdmin):
	inlines = [
        ObjectTextInline
    ]


class IconAdmin(admin.ModelAdmin):
	readonly_fields = ('created', 'updated')
	pass



class EventAdminForm(forms.ModelForm):
    title = forms.CharField()
    annonce = forms.CharField(widget=forms.Textarea, required=False)
    content = forms.CharField(widget=forms.Textarea)
    exclude=('created_class',)

    # для икон. заголовок иконы и сама икона
    icon_file = forms.ImageField()
    icon_title = forms.CharField()


    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        text = system_model.MfSystemObjectText.objects.get(system_object_id=instance.id,status=u'Active').system_text
        self.initial['title'] = text.title
        self.initial['annonce'] = text.annonce
        self.initial['content'] = text.content
        self.initial['icon_title'] = u'Икона '+text.content

    class Meta:
    	# указываем что эта таблица расширяет EventAdminForm
    	model = calendar_model.MfCalendarEvent



class MfCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    readonly_fields = ('created', 'updated','created_class', 'function')
    inlines = [
        ObjectTextInline,RelatedObjectsInline
    ]
 	#exclude=('related_objects',)

    fieldsets=(
    	(None, {'fields':('title', 'function', 'periodic')}),
    	('Контент', {'classes': ('collapse',),'fields':('annonce','content')}),
    	('Настройки', {'classes': ('collapse',),'fields':('status', 'created','updated','created_class')}),
    	('Икона', {'classes': ('collapse',),'fields':('icon_title','icon_file')}),

    )

    form = EventAdminForm

    def save_text(self, request, obj, form, change):
    	text = system_model.MfSystemObjectText.objects.get(system_object_id=obj.id,status=u'Active').system_text
    	text.title = form.cleaned_data['title']
    	text.save()

    def save_model(self, request, obj, form, change):
    	super(MfCalendarEventAdmin, self).save_model(request, obj, form, change)
    	self.save_text(request, obj, form, change)




admin.site.register(system_model.MfSystemRelationType, MfSystemRelationTypeAdmin)
admin.site.register(calendar_model.MfCalendarEvent, MfCalendarEventAdmin)
admin.site.register(system_model.MfSystemText, TextAdmin)
admin.site.register(calendar_model.MfCalendarIcon, IconAdmin)
