#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Xian Wu
# mail: wuxian94@pku.edu.cn
#

"""
SubscriberMaster, the core of the UniSubscriber framework.
It maintains two list, which are monitors and announcers, and dispatch all the messages generated by monitors to all
announcers.
When using master, you can use add, del, activate and deactivate to control monitors and announcers by their names and
you can use start and stop to control the master proc, which is in charge of the message dispatching and all monitors
and announcers.
Do never modify monitor and announcer list(in fact a dict) by direct operation.
"""

from multiprocessing import Process
from multiprocessing import Queue

from Announcer import BaseAnnouncer
from Monitor import BaseMonitor
from utils import StreamLogger
from utils import key_check


class SubscriberMaster(object):
    def __init__(self, name):
        self.__name = name
        self.__monitors = {}
        self.__announcers = {}

        self.__activated_item = set()

        self.monitor_msg_queue = Queue()
        self.announcer_msg_queue = Queue()

        self.logger = StreamLogger.getLogger('(SubscriberMaster){}'.format(name))
        self.proc = Process(target=self.msg_dispatch_proc)

    @property
    def name(self):
        return self.__name

    def _add_item(self, item_dict, item, base_class, msg_queue):
        if not isinstance(item, base_class):
            self.logger.error('%s is not a valid %s with type %s', str(item), base_class.__name__, type(item))
            raise ValueError
        if item.name in item_dict:
            self.logger.error('%s already in %s list.', item.name, base_class.__name__)
            raise KeyError
        if base_class is BaseMonitor:
            item.msg_queue = msg_queue
        item_dict[item.name] = item

    @key_check
    def _del_item(self, item_dict, name, base_class):
        if base_class.__name__+name in self.__activated_item:
            self.logger.warning('Deleting active item: %s, auto deactivated.', name)
            self._deactivate_item(item_dict, name, base_class)
        del item_dict[name]

    @key_check
    def _activate_item(self, item_dict, name, base_class):
        self.__activated_item.add(base_class.__name__+name)
        item_dict[name].start()

    @key_check
    def _deactivate_item(self, item_dict, name, base_class):
        self.__activated_item.remove(base_class.__name__+name)
        item_dict[name].terminate()

    def add_monitor(self, monitor):
        return self._add_item(self.__monitors, monitor, BaseMonitor, self.monitor_msg_queue)

    def add_announcer(self, announcer):
        return self._add_item(self.__announcers, announcer, BaseAnnouncer, self.announcer_msg_queue)

    def del_monitor(self, name):
        return self._del_item(self.__monitors, name, BaseMonitor)

    def del_announcer(self, name):
        return self._del_item(self.__announcers, name, BaseAnnouncer)

    def activate_monitor(self, name):
        return self._activate_item(self.__monitors, name, BaseMonitor)

    def activate_announcer(self, name):
        return self._activate_item(self.__announcers, name, BaseAnnouncer)

    def deactivate_monitor(self, name):
        return self._deactivate_item(self.__monitors, name, BaseMonitor)

    def deactivate_announcer(self, name):
        return self._deactivate_item(self.__announcers, name, BaseAnnouncer)

    def msg_dispatch_proc(self):
        while True:
            msg = self.monitor_msg_queue.get()
            self.logger.info('Msg received.')
            self.logger.debug(msg)
            for announcer in self.__announcers:
                if 'BaseAnnouncer'+announcer in self.__activated_item:
                    self.__announcers[announcer].msg_queue.put(msg)

    def start(self):
        for name in self.__monitors:
            self.activate_monitor(name)
        for name in self.__announcers:
            self.activate_announcer(name)
        self.proc.start()
        self.logger.info('%s(%s) has been started.', self.name, self.proc.pid)

    def join(self):
        self.proc.join()

    def stop(self):
        for name in self.__monitors:
            self.deactivate_monitor(name)
        for name in self.__announcers:
            self.deactivate_announcer(name)
        self.proc.terminate()
        self.logger.info('%s(%s) has been terminated.', self.name, self.proc.pid)