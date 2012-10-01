from django.contrib import admin
from system.models import MfSystemRelationType
from ocalendar import models as calendarModel

class MfSystemRelationTypeAdmin(admin.ModelAdmin):
    list_display = ('id','relation_name')
   
class MfCalendarEventAdmin(admin.ModelAdmin):
	list_display = ('id','title')


admin.site.register(MfSystemRelationType, MfSystemRelationTypeAdmin)
admin.site.register(calendarModel.MfCalendarEvent, MfCalendarEventAdmin)
