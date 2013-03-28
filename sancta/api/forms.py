# -*- coding: utf-8 -*-
# pylint: disable=R0924
from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Тема письма',
        required=False
    )
    message = forms.CharField(
        label='сообщение',
        widget=forms.widgets.Textarea(),
        error_messages={'required': 'сообщение обязательно'}
    )
    sender = forms.EmailField(
        label='ваш email',
        error_messages={
            'required': 'укажите ваш email для того, '
                        'чтобы мы могли ответить вам',
            'invalid': 'введите корректный email'
        }
    )


class ApiEmailNotificate(forms.Form):
    email = forms.EmailField(
        label='ваш email',
        error_messages={
            'required': 'это обязательное поле',
            'invalid': 'введите корректный email'
        }
    )
