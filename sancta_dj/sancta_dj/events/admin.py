from django.contrib import admin
from sancta_dj.sancta.models import MfSystemArticle, MfCalendarEvent, MfSystemRelationType, MfSystemRelation

class MfSystemArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title')


class MfSystemRelationTypeAdmin(admin.ModelAdmin):
    list_display = ('id','relation_type')

class MfCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('id','title')



admin.site.register(MfSystemArticle, MfSystemArticleAdmin)
admin.site.register(MfCalendarEvent, MfCalendarEventAdmin)
admin.site.register(MfSystemRelationType, MfSystemRelationTypeAdmin)
admin.site.register(MfSystemRelation)