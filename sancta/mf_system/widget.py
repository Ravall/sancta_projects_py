# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from mf_system import models as system_model
from mf_calendar import models as calendar_model

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
        return mark_safe(
            '<a href="/admin/sancta/mfcalendaricon/'+str(icon.id)+'/">'+icon.get_title()+'</a><br/>' \
            + '<img width=100px src="/media/crop/150x200/%s">' % icon.image) + '<br/>' \
            + '<i>'+icon.get_annonce()+'</i>' \
            + hidden.render(name, value)


class ImageWidget(forms.FileInput):
    '''
    для поля imageField значение изображения лучше выводить в виде картинки.
    '''
    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):

            output.append(('<a target="_blank" href="/media/crop/150x200/%s">'
                           '<img src="/media/crop/150x200/%s"/></a> '
                           % (value, value)))
        output.append(super(ImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))



class EventLinkWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        if not value:
            return ''
        hidden = forms.HiddenInput(attrs)
        text = system_model.MfSystemObjectText.objects.get(system_object_id=value,status=u'Active').system_text
        return mark_safe(
            '<a href="/admin/sancta/mfcalendarevent/'+str(value)+'">' + text.title + '</a><br/>' + hidden.render(name, value)
        )