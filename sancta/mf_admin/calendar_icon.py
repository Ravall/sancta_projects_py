# -*- coding: utf-8 -*-
from mf_admin.object import ObjectAdmin, ObjectForm, StatusObjectFilter
from mf_admin.calendar_event import EventRelatedInline
from mf_calendar.models import MfCalendarIcon
from mf_system import widget
from hell import sabnac


class RelatedInlineEvent(EventRelatedInline):
    '''
    когда редактируем икону нужно вывести связанные с ней события
    '''
    fields = 'parent_object',
    fk_name = "mf_object"
    verbose_name_plural = 'Икона принадлежит статьям:'

    def formfield_for_dbfield(self, db_field, **kwargs):
        # pylint: disable=E1002
        """
        переопределим отображение некоторых полей в инлайн-форме:
        id сделаем ссылкой
        """
        if db_field.name == 'parent_object':
            kwargs['widget'] = widget.EventLinkWidget()
        return super(RelatedInlineEvent, self).formfield_for_dbfield(
            db_field, **kwargs
        )

    def has_add_permission(self, request):
        # pylint: disable=E1002
        """
        так как иконы добавляются в форме самого события,
        отдельно выводить кнопку "добавить" не нужно
        """
        super(RelatedInlineEvent, self).has_add_permission(request)
        return False


class IconAdminForm(ObjectForm):
    def __init__(self, *args, **kwargs):
        # pylint: disable=E1002,E1101
        super(IconAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        self.set_initial(instance)

    class Meta:
        # указываем что эта таблица расширяет MfCalendarIcon
        model = MfCalendarIcon


class IconAdmin(ObjectAdmin):
    fieldsets = (
        (None, {'fields': ('image', 'title',)}),
        ('Контент', {
            'classes': ('collapse'),
            'fields': ('annonce', 'content')
        }),
        ('Настройки', {
            'classes': ('collapse',),
            'fields': ('status', 'created', 'updated', 'created_class')
        }),
    )
    form = IconAdminForm
    inlines = RelatedInlineEvent,
    list_filter = StatusObjectFilter,

    def save_model(self, request, obj, form, change):
        # pylint: disable=E1002
        # чистка кэша
        sabnac.update_icon.delay(obj, form.cleaned_data)
        super(IconAdmin, self).save_model(
            request, obj, form, change
        )
