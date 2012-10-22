# -*- coding: utf-8 -*-

class Sancta_Router(object):
    """
    A router to control all database operations on models in
    the interface application
    """
    def db_for_read(self, model, **hints):
        "Point all operations on dbrouter models to 'a1lite_mysql'"
        if model._meta.app_label == 'sancta':
            return 'sancta_db'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on dbrouter models to 'a1lite_mysql'"
        if model._meta.app_label == 'sancta':
            return 'sancta_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in dbrouter is involved"
        if obj1._meta.app_label == 'sancta' \
                or obj2._meta.app_label == 'sancta':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the dbrouter app only appears on the 'dbrouter_psql' db"
        if db == 'sancta_db':
            return False
        if model._meta.app_label == "sancta":
            return False
        return None