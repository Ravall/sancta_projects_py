# -*- coding: utf-8 -*-
# pylint: disable=E1102
'''
АЗАЗЕЛЬ - Главный Знаменосец адского войска.
-----
    синхронизирует папки с изображениями. обрезая оригинальные
    sunc_folders - синхронизировать папки
'''


import os
import re
from sets import Set
from django.conf import settings
import celery
import logging


@celery.task()
def sync_folders():
    daemon = AzazelDaemon()
    daemon.sunc_folders()


class AzazelDaemon():
    '''
    демон азазель, синхронизирует и ресайзит изображения.
    проверяет изменение в папке origin (новые и удаленные изображения)
    и раскидывает кропнутые изображения по нужным папкам

    нужные папки - это папки формата 000x000 находящиеся в папке crop
                и папки в из дополнительного списка add_sync_folders
    настройка
        origin_folder - оригинальная папка
        sync_folder куда нужно синхронизировать
        add_sync_folders - дополнительные папки
    '''

    #папка куда нужно синхронизировать
    sync_folder = os.path.abspath(
        os.path.join(settings.MEDIA_ROOT, 'crop')
    )
    # папка откуда берем изображения,
    # которые нужно синхронизировать
    origin_folder = os.path.abspath(
        os.path.join(settings.MEDIA_ROOT, 'origin')
    )
    #дополнительные папки, куда нужно
    #синхронизировать изображения
    add_sync_folders = []

    # список оригинальных фалов.
    #заполняется в ходе работы
    origin_image_list = []

    def __init__(self):
        self.logger = logging.getLogger('sancta_log')

    def get_folders_to_sync(self):
        '''
        получаем список папок, куда нужно синхронизавть.
        список берем из dir (где храняться кропнутые изображения)
        добавляем дополнительные папки
        (мало-ли, если придется синхронизировать куда-нибудь кроме этого)
        из списка берем только те которые удовлетвояют виду 000x000
        '''
        folders = map(
            lambda folder_name: self.sync_folder + '/' + folder_name,
            os.listdir(self.sync_folder)) + self.add_sync_folders
        self.logger.info("folders list:" + str(folders))
        return filter(
            lambda folder: re.match(r'^\d{,4}x\d{,4}$', folder.split('/')[-1]),
            folders)

    def folder_sync(self, folder):
        '''
        синхронизатор папки. Для папки, мы проходимся и смотрим
        какие файлы появились в оригинальной и их нужно синхронизировать,
        какие нужно удалить - если они есть в синхронизируемой, но отсутсвуют
        в оригинальной
        '''
        self.logger.info("обработка для папки :" + folder)
        # файлы в папке
        folder_image_list = os.listdir(folder)
        # файлы которые есть в origin_image_list но нет в folder_image_list
        new_files = Set(self.origin_image_list) - Set(folder_image_list)
        self.logger.info("новые файлы :" + str(new_files))
        # добавляем
        for file_to_sync in new_files:
            #получаем размеры нужного изображения из имени папки
            size = folder.split('/')[-1]
            # ресайзим по-умному
            command = 'convert "{0}" -resize "{1}^"  -gravity center ' \
                      ' -extent {1} -filter Blackman -modulate 110,102,100' \
                      ' -sharpen 1x1 -enhance  "{2}"'.format(
                      self.origin_folder + '/' + file_to_sync,
                      size, folder + '/' + file_to_sync)
            self.logger.info(command)
            result = os.system(command)
            self.logger.info(result)
        # файлы которые есть в folder_image_list но нет в origin_image_list
        delte_files = Set(folder_image_list) - Set(self.origin_image_list)
        self.logger.info("устаревшие файлы:" + str(delte_files))
        # удаляем
        for file_to_sync in delte_files:
            self.logger.info('delete ' + folder + '/' + file_to_sync)
            os.remove(folder + '/' + file_to_sync)

    def sunc_folders(self):
        '''
        основной метод
        проходимся по всем папкам и для кадой запускаем синхронизатор
        '''
        #запоминаем список файлов  в оригинальной директории
        self.logger.info("start azazel")
        self.origin_image_list = os.listdir(self.origin_folder)
        #проходим по каждой папке и запускаем синхронизатор
        for folder in self.get_folders_to_sync():
            self.folder_sync(folder)
        self.logger.info("stop azazel")
