#!/usr/bin/env pythstohison
# coding: utf-8

import re
import rumps
from timer import Timer
from config import *


class MultiTimerApp(rumps.App):
    def __init__(self):
        super(MultiTimerApp, self).__init__(APP_TITLE,
                                            icon=PATH_RES_IMG_MY_TIME_ALPHA)

        self.menu = [MENU_ITEM_ADD_TIMER, MENU_ITEM_REMOVE_TIMER]
        self.timers = []

    @rumps.timer(UPDATE_VIEW_INTERVAL)
    def _update_view(self, _):
        if len(self.timers) == 0:
            self.title = APP_TITLE
        else:
            title = ''
            for timer in self.timers:
                title += TIME_VIEW_FORMAT.format(
                    timer.title.split('[')[0],
                    MultiTimerApp.sec_to_hms(timer.current_sec))
            self.title = title

    @rumps.clicked(MENU_ITEM_ADD_TIMER)
    def _add_timer(self, _):
        window_title = rumps.Window(title=WINDOW_TITLE_MESSAGE,
                                    message='',
                                    default_text='',
                                    cancel=True,
                                    dimensions=WINDOW_DIM)
        window_title.icon = PATH_RES_IMG_MY_TIME
        res_title = window_title.run()
        if not res_title.clicked:
            return

        sec = None
        while sec is None:
            window_sec = rumps.Window(title=WINDOW_TIME_MESSAGE,
                                      message='',
                                      default_text=TIME_EXAMPLE,
                                      cancel=True,
                                      dimensions=WINDOW_DIM)
            window_sec.icon = PATH_RES_IMG_MY_TIME
            res_sec = window_sec.run()
            if not res_sec.clicked:
                return

            try:
                sec = MultiTimerApp.hms_to_sec(res_sec.text)
            except TypeError:
                rumps.alert(INVALID_TIME_FORMAT_MESSAGE)

        title = res_title.text

        def on_finish():
            self._update_view(None)
            rumps.alert(TIME_FINISHED_FORMAT.format(title))
            self._stop_timer(self._get_timer(title))

        self.timers.append(Timer(title, sec, on_finish))
        self.menu.add(rumps.MenuItem(title=title,
                                     callback=self._switch_timer,
                                     icon=PATH_RES_IMG_PLAY))

        remove_menu = self.menu[MENU_ITEM_REMOVE_TIMER]
        remove_menu.set_callback(lambda: None)
        remove_menu.add(rumps.MenuItem(title, callback=self._remove_timer))

    def _remove_timer(self, sender):
        for timer in self.timers:
            if sender.title == timer.title:
                # 別スレッドが生成され続けるのを防ぐため、timerはストップ
                timer.stop()
                self.timers.remove(timer)
                self.menu.pop(timer.title)
                self.menu[MENU_ITEM_REMOVE_TIMER].pop(timer.title)
                break
        if len(self.timers) == 0:
            self.menu[MENU_ITEM_REMOVE_TIMER].set_callback(None)

    def _get_timer(self, title):
        for timer in self.timers:
            if title == timer.title:
                return timer

    def _switch_timer(self, sender):
        timer = self._get_timer(sender.title)
        if timer.state in [Timer.STATE_PAUSE, Timer.STATE_STOP]:
            self._start_timer(timer)
        else:
            self._pause_timer(timer)

    def _start_timer(self, timer):
        timer.start()
        self.menu[timer.title].icon = PATH_RES_IMG_PAUSE

    def _stop_timer(self, timer):
        timer.stop()
        self.menu[timer.title].icon = PATH_RES_IMG_PLAY

    def _pause_timer(self, timer):
        timer.pause()
        self.menu[timer.title].icon = PATH_RES_IMG_PLAY

    @staticmethod
    def hms_to_sec(hms):
        m = re.match(r'\d{2}:\d{2}:\d{2}', hms)
        if m is not None:
            h, m, s = map(int, hms.split(':'))
            return h * 3600 + m * 60 + s
        else:
            raise TypeError

    @staticmethod
    def sec_to_hms(sec):
        h, mod = divmod(sec, 3600)
        m, s = divmod(mod, 60)
        form = "{0:02d}:{1:02d}:{2:02d}".format(h, m, s) \
            if h > 0 else "{0:02d}:{1:02d}".format(m, s)
        return form
