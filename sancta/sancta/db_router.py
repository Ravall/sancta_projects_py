# -*- coding: utf-8 -*-


class Sancta_Router(object):
    sancta_db_apps = 'sancta', 'taggit', 'api'
    sancta_db_syncapps = 'taggit'
    """
    A router to control all database operations on models in
    the interface application
    """
    def db_for_read(self, model, **hints):
        "Point all operations on dbrouter models to 'a1lite_mysql'"
        if model._meta.app_label in self.sancta_db_apps:
            return 'sancta_db'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on dbrouter models to 'a1lite_mysql'"
        if model._meta.app_label in self.sancta_db_apps:
            return 'sancta_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in dbrouter is involved"
        if obj1._meta.app_label in self.sancta_db_apps\
                or obj2._meta.app_label in self.sancta_db_apps:
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the dbrouter app only appears on the 'dbrouter_psql' db"
        if model._meta.app_label in self.sancta_db_syncapps:
           # syncdb только для особых приложений
            return db == 'sancta_db'
        if model._meta.app_label in self.sancta_db_apps:
            return False
        if db == 'sancta_db':
            return False
        return None
