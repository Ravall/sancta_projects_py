# -*- coding: utf-8 -*-
from hell.anubis import generate_sitemap_file
from django.shortcuts import redirect
from django.contrib import messages

def generate_sitemap_view(request):
    messages.add_message(
        request, messages.SUCCESS,
        'задание перегенерить карту сайта поставлено.'
    )
    generate_sitemap_file.delay()
    return redirect('/admin/')