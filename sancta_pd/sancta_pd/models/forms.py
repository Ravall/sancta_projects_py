# -*- coding: utf-8 -*-
"""
формы.
"""
import deform
import colander
from deform.interfaces import FileUploadTempStore


class MemoryTmpStore(dict):
       """ Instances of this class implement the
       :class:`deform.interfaces.FileUploadTempStore` interface"""
       def preview_url(self, uid):
           return None

tmpstore = MemoryTmpStore()
# tmpstore = FileUploadTempStore()

def form_error(form, key, text):
     exc = colander.Invalid(form, text)
     exc[key] = text
     return exc



def form_icon_upload(**kwargs):
    def preparer_alt(value):
        print value
        pass;

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
            preparer=preparer_alt,
            widget=deform.widget.TextInputWidget(),
        )
        alt = colander.SchemaNode(
            colander.String(),
            title=u"alt",
            description=u'аlt тег',
            widget=deform.widget.TextInputWidget(),
            missing=None,
        )
        upload = colander.SchemaNode(
            deform.FileData(),
            title=u"Файл Иконы",
            widget=deform.widget.FileUploadWidget(tmpstore),
            missing=None,
        )
        fileurl = colander.SchemaNode(
            colander.String(),
            title=u"url картинки чтобы скомуниздить",
            description=u'либо файл грузите либо url давайте',
            widget=deform.widget.TextInputWidget(),
            missing=None,
        )



    def validator(form, value):
        if (value.get('fileurl') and value.get('upload')) or (not value.get('fileurl') and not value.get('upload')):
            raise form_error(form, 'fileurl', 'либо url, либо file. Ты уж определись')

        if not value.get('upload').get('mimetype') == 'image/jpeg':
            raise form_error(form, 'upload', 'Изображение должно быть загружено в формате jpg')
        pass;


    return deform.Form(
        IconUpload(validator=validator),
        buttons=(
            deform.Button(type='submit',value=u'load',name=u'load'),
        ),
        bootstrap_form_style='form-horizontal'
    )