# -*- coding: utf-8 -*-

def icon_table():
    '''
    к существующему запросу, присоединим таблицу с иконами
    '''
    return {
        'select': {
            'id': 'mf_calendar_icon.id',
            'image': 'mf_system_object.image',
            'event_id': 'mf_system_relation.parent_object_id'
        },
        'tables': [
            'mf_calendar_icon',
        ],
        'where': [
            'mf_calendar_icon.mfsystemobject_ptr_id = mf_system_object.id'
        ]
    }