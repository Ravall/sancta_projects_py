# -*- coding: utf-8 -*-


def is_column_exists(db_connect, db_name, column):
    result = db_connect.execute(
        "SHOW COLUMNS FROM `{0}` LIKE '{1}'".format(
            db_name, column
        )
    )
    return bool(result)


def is_table_exists(db_connect, db_table):
    return (db_table,) in db_connect.execute('show tables')
