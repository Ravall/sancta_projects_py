# -*- coding: utf-8 -*-
from django.contrib import admin


class MfSystemRelationTypeAdmin(admin.ModelAdmin):
    list_display = 'id', 'relation_name'
