from django.contrib import admin
from django.contrib.contenttypes import generic
from mf_system import models as system_model
from mf_calendar import models as calendar_model

class MfSystemRelationTypeAdmin(admin.ModelAdmin):
    list_display = ('id','relation_name')

class ObjectTextInline(admin.TabularInline):
    model = calendar_model.MfCalendarEvent.texts.through
    extra = 0

class RelatedObjectsInline(admin.TabularInline):
    model = calendar_model.MfCalendarEvent.related_objects.through
    extra = 0

class TextAdmin(admin.ModelAdmin):
	inlines = [
        ObjectTextInline,
    ]



class MfCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    readonly_fields = ('created', 'updated')
    inlines = [
        ObjectTextInline
    ]
    exclude=('texts', 'created_class')


admin.site.register(system_model.MfSystemRelationType, MfSystemRelationTypeAdmin)
admin.site.register(calendar_model.MfCalendarEvent, MfCalendarEventAdmin)
admin.site.register(system_model.MfSystemText, TextAdmin)
