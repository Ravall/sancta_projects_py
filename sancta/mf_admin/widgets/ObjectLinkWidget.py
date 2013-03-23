# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from mf_system.models.mf_object import MfSystemObject


class ObjectLinkWidget(forms.Widget):
    """
    Виджет отображения ссылки на редактирование
    """
    def render(self, name, value, attrs=None):
        if not value:
            return ''
        hidden = forms.HiddenInput(attrs)
        mf_object = MfSystemObject.objects.get(pk=value)
        if mf_object.created_class == 'MfCalendarEvent':
            return mark_safe(
                u'событие: <a href="/admin/sancta/mfcalendarevent/{0}">{1}</a>'
                '<br/>{2}'.format(
                    str(value),
                    mf_object.get_title(),
                    hidden.render(name, value)
                )
            )
        return '#{0} ({1})'.format(str(value), mf_object.created_class)
