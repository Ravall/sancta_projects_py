# -*- coding: utf-8 -*-
from django.contrib import admin
from mf_calendar.models import MfCalendarIcon, MfCalendarEvent
from mf_system.models import MfSystemRelationType, MfSystemArticle
from mf_admin.calendar_icon import IconAdmin
from mf_admin.system_relation_type import MfSystemRelationTypeAdmin
from mf_admin.calendar_event import MfCalendarEventAdmin
from mf_admin.system_article import MfSystemArticleAdmin


admin.site.register(MfCalendarIcon, IconAdmin)
admin.site.register(MfSystemRelationType, MfSystemRelationTypeAdmin)
admin.site.register(MfCalendarEvent, MfCalendarEventAdmin)
admin.site.register(MfSystemArticle, MfSystemArticleAdmin)

