# -*- coding: utf-8 -*-
import os
from tools.grammar import translite
from hell import azazel
from django.conf import settings


def handle_uploaded_file(request_file, icon_title):
    '''
    загружаем файл из request, сохраняем с уникальным именем
    очищаем exif данные
    '''
    def upload_file(request_file, new_filename):
        '''
        берем из request файл и грузим его в нужную папку
        '''
        destination = open(
            settings.ORIGIN_MEDIA_ROOT + '/' + new_filename, 'wb+'
        )
        for chunk in request_file.chunks():
            destination.write(chunk)
        destination.close()

    def create_new_filename(request_filename, icon_title):
        '''
        создаем имя файла - транслитерированный заголовок,
        и добавляем суффикс, если такой файл существует
        '''
        # разделяем имя файла и его расширение
        file_name_info = os.path.splitext(request_filename)
        # создаем шаблон имени файла
        new_filename = translite(icon_title) + '%s' + file_name_info[1]
        prefix_filename = new_filename % ''
        count_try = 0
        while os.path.exists(
            settings.ORIGIN_MEDIA_ROOT + '/' + prefix_filename
        ):
            count_try += 1
            prefix_filename = new_filename % count_try
        return prefix_filename

    # генерируем уникальное имя файла
    new_filename = create_new_filename(request_file.name, icon_title)
    # загружаем файл
    upload_file(request_file, new_filename)
    ## удаляем мета теги и перемещаем в новую папку
    os.system('exiftool -all= ' + new_filename)
    # вызываем отложенное задание синхронизации
    azazel.sync_folders.delay()
    return new_filename
