# -*- coding: utf-8 -*-
from sancta_pd.models.db_models import *
from sancta_pd.models.forms import *
from pyramid.view import view_config
from pyramid.path import AssetResolver
import shutil
import colander


@view_config(route_name="event_list", renderer='event/list.jinja2')
def list(request):
    return {'event_list' : Event.get_all(),}


@view_config(route_name="event_edit", renderer='event/edit.jinja2')
def edit(request):
    event_id = request.matchdict['id']
    return {
        'id': event_id,
    }


@view_config(route_name="event_add_icon", renderer='event/addicon.jinja2')
def addicon(request):
    event_id = request.matchdict['id']
    form = form_icon_upload(default_title='name')
    if 'load' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)  # call validate
            print appstruct.get('file')
            #path = AssetResolver()
            #fp = appstruct.get('upload').get('fp')
            #fp_new = open(path.resolve('sancta_pd:static/images/origin/%s.jpg ' % appstruct.get('filename')).abspath(),'w+b')
            #shutil.copyfileobj(fp, fp_new)
        except deform.ValidationFailure, error_form: # catch the exception
            '''
            ошибка в defrom есть сама форма, но заполненная
            '''
            form = error_form
    return {
        'event_id': event_id,
        'form': form.render(),
    }
