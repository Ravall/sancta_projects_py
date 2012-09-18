# -*- coding: utf-8 -*-
from sancta_pd.models.db_models import *
from sancta_pd.models.forms import *
from pyramid.view import view_config



@view_config(route_name="event_list", renderer='event/list.jinja2')
def list(request):
    return {'event_list' : Event.get_all(),}


@view_config(route_name="event_edit", renderer='event/edit.jinja2')
def edit(request):
	form = form_icon_upload(default_title='name')
	event_id = request.matchdict['id']
	return {
		'id': event_id,
		'form': form
	}