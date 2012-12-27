# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from mf_system.models.mf_object_text import MfSystemObjectText
from mf_calendar import models as calendar_model
from sancta.templatetags.image_exists import image_tag
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
                u'<a href="/admin/sancta/mfcalendarevent/{0}">{1}</a>'
                '<br/>{2}'.format(
                    str(value),
                    mf_object.get_title(),
                    hidden.render(name, value)
                )
            )
        return '#{0} ({1})'.format(str(value), mf_object.created_class)


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

        return image_tag(icon.image, 'crop/150x200') + hidden.render(name, value)


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
        text = MfSystemObjectText.objects.get(
            system_object_id=value,
            status=u'Active'
        ).system_text
        return mark_safe(
            u'<a href="/admin/sancta/mfcalendarevent/{0}">{1}</a>'
            '<br/>{2}'.format(
                str(value), text.title, hidden.render(name, value)
            )
        )


class ArticleLinkWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        if not value:
            return ':-)'
        hidden = forms.HiddenInput(attrs)
        text = MfSystemObjectText.objects.get(
            system_object_id=value,
            status=u'Active'
        ).system_text
        return mark_safe(
            u'<a href="/admin/sancta/mfsystemarticle/{0}">{1}</a>'
            '<br/>{2}'.format(
                str(value), text.title, hidden.render(name, value)
            )
        )
