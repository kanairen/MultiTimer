#!/usr/bin/env python
# coding: utf-8

import time
import threading


class Timer(object):
    STATE_RUNNING = 'running'
    STATE_PAUSE = 'pause'
    STATE_STOP = 'stop'

    def __init__(self, title, sec, on_finish):
        self.title = title
        self._init_sec = sec
        self.current_sec = sec
        self.state = Timer.STATE_STOP
        self.on_finish = on_finish

    def start(self):
        self.state = Timer.STATE_RUNNING

        def count():
            while True:
                time.sleep(1)
                if self.state == Timer.STATE_RUNNING:
                    self.current_sec -= 1
                else:
                    break
                if self.current_sec <= 0:
                    self.on_finish()
                    return

        threading.Thread(target=count).start()

    def pause(self):
        self.state = Timer.STATE_PAUSE

    def stop(self):
        self.state = Timer.STATE_STOP
        self.current_sec = self._init_sec


