# -*- coding: utf-8 -*-
from sancta_pd.models import db_models
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from sancta_pd.models import app

class mf:
    '''
    родитель, хранящий коннекты
    '''
    connection = False

    def __init(self):
        '''
        по умолчанию соединение устанавливается из конфига пирамиды
        но не всегда он есть. например, когда гоняешь тесты, тогда
        нужно конфиг ставить в ручную
        '''
        self.connection = app.get_config('sqlalchemy.url')

    def set_connection(self, connection):
        '''
        устанавливаем конфиг подключения к бд вручную
        '''
        self.connection = connection


    def get_session(self):
        '''
        получаем сессию бд
        '''
        Session = sessionmaker(bind=create_engine(self.connection))
        return Session()

class mfObject(mf):
    def create_object(self, title='', annonce='', content=''):
        p_object = db_models.Object(created_class=self.created_class)
        p_object.text.append(
            db_models.TextObjectAssociation(
                text=db_models.Text(title=title, annonce=annonce, content=content)
            )
        )
        return p_object

class mfFile(mfObject):
    created_class = 'mf_system_file'
    def create_file(self, **kwargs):
        
        # создаем файл, текст, объект, 
        # привязываем текст объект к тексту и связываем файл с объектом. 
        # охренеть!
        db_file = db_models.FileObject(
            file_name=kwargs['file'],
            object=self.create_object(
                title=kwargs['title'], annonce=kwargs['annonce']
            )
        )


        return db_file


class mfEvent(mfObject):
    id = False
    def __init(self, id):
        self.id = id

    def add_icon(self, **kwargs):
        session = self.get_session()

        event = session.query(db_models.Event).get(self.id)
        
        mf_file = mfFile()
        db_file = mf_file.create_file(
            title=kwargs['title'], annonce=kwargs['alt'], file=kwargs['file']
        )
        event.icons.add(db_file)

        session.add(db_file);


        session.commit()
        return db_file
        
