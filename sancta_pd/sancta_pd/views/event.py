# -*- coding: utf-8 -*-
from sancta_pd.models import *
from pyramid.view import view_config

import deform
import colander

class MemoryTmpStore(dict):
    """ Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface"""
    def preview_url(self, uid):
        return None

tmpstore = MemoryTmpStore()


class IconUpload(colander.Schema):
	title = colander.SchemaNode(
	    colander.String(),
	    title=u"Заголовок",
	    description=u'Название иконы',
	    widget=deform.widget.TextInputWidget(),
	)
	upload = colander.SchemaNode(
        deform.FileData(),
        title=u"Файл Иконы",
        widget=deform.widget.FileUploadWidget(tmpstore)
    )


def form_icon_upload():
	return deform.Form(
		IconUpload(),
		buttons=(
			deform.Button(type='submit',value=u'Загрузить',name=u'Загрузить'),
			deform.Button(type='reset',value=u'Отмена',name=u'Отмена')
		),
		bootstrap_form_style='form-horizontal'
	)



@view_config(route_name="event_list", renderer='event/list.jinja2')
def list(request):
    return {'event_list' : Event.get_all(),}


@view_config(route_name="event_edit", renderer='event/edit.jinja2')
def edit(request):
	form = form_icon_upload()
	event_id = request.matchdict['id']
	return {
		'id': event_id,
		'form': form
	}