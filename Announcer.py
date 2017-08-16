#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Xian Wu
# mail: wuxian94@pku.edu.cn
#

"""
BaseAnnouncer, base class of all the other announcer class.
One should never instantialize a announcer with type BaseAnnouncer but should derive a class from BaseAnnouncer.
When deriving a class, you are expected to implement all the abstract methods and follow the conventions:
    1. in the __init__ function, you should pass a unique 'name' to the super class, other parts of the subscriber
    will use name to identify every announcer.
    2. in the announce function, you are expected to implement the announcing method. You can do whatever you want
    in this function, maybe sending an email, popping a msg box or even sending an WeChat message. You will only get
    a variable msg as the parameter. This is a tuple with two items. The first is the monitor's name and the second
     is a dict-like object and we can guarantee that it contains following item:
        prev_content: extracted content before changes happened
        new_content: extracted content after changes happened
        diff_content: differences between the two contents above, defined by monitor
       and the following is what we encourage a monitor to pass:
        msg: a brief description about this msg, such as "new item detected"
        status: a status code denoting your monitor status, we use 0 to denote that everything is ok
"""

from abc import abstractmethod, ABCMeta
from multiprocessing import Process

from multiprocessing import Queue

from utils import StreamLogger


class BaseAnnouncer(object):
    __metaclass__ = ABCMeta
    ROOT_MSG_QUEUE = Queue()

    def __init__(self, name, msg_queue=ROOT_MSG_QUEUE):
        self.__name = name
        self.msg_queue = msg_queue

        self.logger = StreamLogger.getLogger('(Announcer){}'.format(name))
        self.proc = Process(target=self.announcer_proc)

    @property
    def name(self):
        return self.__name

    def announcer_proc(self):
        while True:
            _msg = self.msg_queue.get()
            self.announce(_msg)

    def start(self):
        self.proc.start()
        self.logger.info('%s(%s) has been started.', self.name, self.proc.pid)

    def terminate(self):
        if self.is_alive():
            self.proc.terminate()
            self.logger.info('%s(%s) has been terminated.', self.name, self.proc.pid)
        else:
            self.logger.info('%s(%s) is not running.', self.name, self.proc.pid)

    def is_alive(self):
        return self.proc.is_alive()

    @abstractmethod
    def announce(self, msg):
        pass
