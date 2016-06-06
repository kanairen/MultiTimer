#!/usr/bin/env python
# coding: utf-8

import os

#PATH
PATH = os.path.join(os.path.dirname(__file__), '..')
PATH_RES = os.path.join(PATH, 'res')

PATH_RES_IMG = os.path.join(PATH_RES, 'img')

PATH_RES_IMG_PAUSE = os.path.join(PATH_RES_IMG, 'pause.png')
PATH_RES_IMG_PLAY = os.path.join(PATH_RES_IMG, 'play.png')
PATH_RES_IMG_STOP = os.path.join(PATH_RES_IMG, 'stop.png')
PATH_RES_IMG_TIME = os.path.join(PATH_RES_IMG, 'time.png')

# App Config
APP_TITLE = ""

UPDATE_VIEW_INTERVAL = 0.1

MENU_ITEM_ADD_TIMER = 'Add Timer'
MENU_ITEM_REMOVE_TIMER = 'Remove Timer'

WINDOW_TITLE_MESSAGE = 'Timer Title'
WINDOW_TIME_MESSAGE = 'Timer Length'
WINDOW_DIM = (320, 20)

TIME_EXAMPLE = '00:00:00'
TIME_VIEW_FORMAT = '{}[ {} ] '
TIME_FINISHED_FORMAT = 'Timer \'{}\' finished.'

INVALID_TIME_FORMAT_MESSAGE = 'Timer length should be input like \'HH:MM:SS\''

