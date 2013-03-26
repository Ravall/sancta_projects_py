# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.reverse import reverse
from mf_calendar.models import MfCalendarEvent
from api import forms
from api.models import NotificationEmail
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def index(request):
    events_count = MfCalendarEvent.objects.filter(status='active').count()
    return render_to_response(
        'api/index.html',
        {
            'events_count': events_count
        },
        context_instance=RequestContext(request)
    )


def docs(request):
    return render_to_response(
        'api/documentation_event.html',
        {
            'event_by_id_example': reverse(
                'event-api', kwargs={
                    'event_id': 29,
                    'format': 'json'
                },
                request=request
            ),
            'event_by_name_example': reverse(
                'event-api', kwargs={
                    'event_id': 'velikiy_post',
                    'format': 'json'
                },
                request=request
            ),
            'event_by_tag_example': reverse(
                'eventtag-api', kwargs={
                    'event_tag': 'tag1',
                    'format': 'json'
                },
                request=request
            ),
            'event_all_example': reverse(
                'eventall-api', kwargs={
                    'format': 'json'
                },
                request=request
            ),
        },
        context_instance=RequestContext(request),

    )


def docs_calendar(request):
    return render_to_response(
        'api/documentation_calendar.html',
        {
            'calendar_example': reverse(
                'calendar-api', kwargs={
                    'day': '2013-01-01',
                    'format': 'json'
                },
                request=request
            ),
        },
        context_instance=RequestContext(request)
    )


def docs_articles(request):
    return render_to_response(
        'api/documentation_article.html',
        {
            'article_by_id_example': reverse(
                'article-api', kwargs={
                    'article_id': 228,
                    'format': 'json'
                },
                request=request
            ),
            'article_by_name_example': reverse(
                'article-api', kwargs={
                    'article_id': 'kak_pitatsya_v_velikiy_post',
                    'format': 'json'
                },
                request=request
            ),
            'article_by_tag_example': reverse(
                'articletag-api', kwargs={
                    'article_tag': 'post',
                    'format': 'json'
                },
                request=request
            ),
        },
        context_instance=RequestContext(request)
    )

def smartdate(request):
    return render_to_response(
        'api/smart_date.html',
        context_instance=RequestContext(request)
    )


def requires(request):
    if request.method == 'POST':
        form = forms.ApiEmailNotificate(request.POST)
        if form.is_valid():
            email = NotificationEmail(
                email = form.cleaned_data['email']
            )
            email.save()
            messages.success(request, 'Ваш еmail добавлен в базу')
            return HttpResponseRedirect('/requires/')
    else:
        form = forms.ApiEmailNotificate()
    return render_to_response(
        'api/requires.html',
        {'form': form},
        context_instance=RequestContext(request)
    )


def contacts(request):
    #pylint: disable=R0924
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            subject = u'api.sancta.ru theme: {0}'.format(
                form.cleaned_data['subject']
            )
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            send_mail(subject, message, sender, [settings.SERVER_EMAIL])
            messages.success(request, 'Ваше письмо отправлено')
            return HttpResponseRedirect('/contacts/')
    else:
        form = forms.ContactForm() # An unbound form

    return render_to_response(
        'api/contacts.html',
        {'form': form},
        context_instance=RequestContext(request)
    )