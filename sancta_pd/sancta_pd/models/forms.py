# -*- coding: utf-8 -*-
"""
формы.
"""
import deform
import colander

class MemoryTmpStore(dict):
    """ Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface"""
    def preview_url(self, uid):
        return None

tmpstore = MemoryTmpStore()


def form_icon_upload(**kwargs):
    """
    форма загрузки иконы
    """
    class IconUpload(colander.Schema):
        title = colander.SchemaNode(
            colander.String(),
            title=u"Заголовок",
            description=u'Название иконы',
            default=kwargs['default_title'],
            widget=deform.widget.TextInputWidget(),
        )
        filename = colander.SchemaNode(
            colander.String(),
            title=u"Название файла",
            description=u'Конечное название jpg файла (транслит)',
            widget=deform.widget.TextInputWidget(),
        )
        alt = colander.SchemaNode(
            colander.String(),
            title=u"alt",
            description=u'аlt тег',
            widget=deform.widget.TextInputWidget(),
        )
        upload = colander.SchemaNode(
            deform.FileData(),
            title=u"Файл Иконы",
            widget=deform.widget.FileUploadWidget(tmpstore)
        )

    return deform.Form(
        IconUpload(),
            buttons=(
                deform.Button(type='submit',value=u'Загрузить',name=u'Загрузить'),
        ),
        bootstrap_form_style='form-horizontal'
    )