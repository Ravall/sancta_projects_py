# -*- coding: utf-8 -*-
"""
формы.
"""
from sancta_pd.models import app
import deform
import colander
import urllib
import trans

from deform.interfaces import FileUploadTempStore
from pyramid.path import AssetResolver

class Seo_Helper:
    '''
    seo помошник. Транслитератор
    '''
    @staticmethod
    def _eu8(string):  
        return string.encode('utf-8')

    @staticmethod
    def traslit(string):    
        return Seo_Helper._eu8(string.replace(' ','-').encode('trans').lower())  



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
        '''
        Упрощаем работу с загруженными файлами. 
        fp от upload или fileurl доступен по ключу file
        '''
        if values.get('upload'):
           values['file'] = values.get('upload').get('fp')
        if values.get('fileurl'):
            values['file'] = values.get('fileurl')
        return values




    def preparer_fileurl(value):
        '''
        открываем файл по web урлу
        '''
        if value:
            fp = urllib.urlopen(value)
        else:
            fp = colander.null
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
            description=u"Конечное название jpg файла (название автоматически транслитерируется(string.replace(' ','-').encode('trans').lower()))",
            widget=deform.widget.TextInputWidget(),
            default=kwargs['default_title'],
            preparer=Seo_Helper.traslit
        )
        alt = colander.SchemaNode(
            colander.String(),
            title=u"alt",
            description=u'аlt тег',
            widget=deform.widget.TextInputWidget(),
            default=kwargs['default_title'],
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
        '''
        валидируем форму
        '''
        # изображение должно быть загружено
        if value.get('fileurl') and value.get('upload'):
            raise form_error(form, 'fileurl', 'либо url, либо file. Ты уж определись')
        if not value.get('fileurl') and not value.get('upload'):
            raise form_error(form, 'fileurl', 'либо url, либо file. Введи уж что-нибудь')

        # проверяем тип загруженного файлам
        if value.get('upload') and not value.get('upload').get('mimetype') == 'image/jpeg':
            raise form_error(form, 'upload', 'Изображение должно быть загружено в формате jpg')
        if value.get('fileurl') and not value.get('fileurl').info().gettype() == 'image/jpeg':
            raise form_error(form, 'fileurl', 'Ну ты чо! тут ссылка должна быть на изображение')

        #проверка на существование файла
        path = AssetResolver()
        if path.resolve(app.get_config('origin_images_path') + '%s.jpg' % value.get('filename')).exists():
            raise form_error(form, 'filename', 'Файл именем  %s.jpg уже есть' % value.get('filename'))

    return deform.Form(
        IconUpload(validator=validator,preparer=file_upload_post_process),
        buttons=(
            deform.Button(type='submit',value=u'load',name=u'load'),
        ),
        bootstrap_form_style='form-horizontal',
        
    )