from django.contrib import admin
from sancta_dj.sancta.models import MfSystemArticle, MfCalendarEvent

class MfSystemArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title')

class MfCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('id','title')


admin.site.register(MfSystemArticle, MfSystemArticleAdmin)
admin.site.register(MfCalendarEvent, MfCalendarEventAdmin)