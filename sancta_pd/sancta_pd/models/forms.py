# -*- coding: utf-8 -*-
"""
формы.
"""
import deform
import colander
import urllib
from deform.interfaces import FileUploadTempStore
from pyramid.path import AssetResolver


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
    def file_upload_post_process(values):
        print values
        #if values.get('upload'):
         #   node['file'] = values.get('upload').get('fp')
        #if kw.get('fileurl'):
         #   node['file'] = values.get('fileurl')
        values['file'] = 'xxx'
        return values




    def preparer_fileurl(value):
        fp = urllib.urlopen(value)
        return fp

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
            preparer=preparer_fileurl,
        )



    def validator(form, value):
        if value.get('fileurl') and value.get('upload'):
            raise form_error(form, 'fileurl', 'либо url, либо file. Ты уж определись')

        if not value.get('fileurl') and not value.get('upload'):
            raise form_error(form, 'fileurl', 'либо url, либо file. Введи уж что-нибудь')

        if value.get('upload') and not value.get('upload').get('mimetype') == 'image/jpeg':
            raise form_error(form, 'upload', 'Изображение должно быть загружено в формате jpg')

        if value.get('fileurl') and not value.get('fileurl').info().gettype() == 'image/jpeg':
            raise form_error(form, 'fileurl', 'Ну ты чо! тут ссылка должна быть на изображение')

        pass;


    return deform.Form(
        IconUpload(validator=validator,flatten=file_upload_post_process),
        buttons=(
            deform.Button(type='submit',value=u'load',name=u'load'),
        ),
        bootstrap_form_style='form-horizontal'
    )