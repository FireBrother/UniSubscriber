#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Xian Wu
# mail: wuxian94@pku.edu.cn
#

import logging


class StreamLogger():
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(name)s: %(message)s', '%Y-%m-%d %H:%M:%S')
    stream_handler.setFormatter(formatter)

    @classmethod
    def getLogger(cls, name):
        logger = logging.getLogger(name)
        logger.addHandler(cls.stream_handler)
        logger.setLevel(logging.INFO)
        return logger


def key_check(func):
    def wrapper(self, item_dict, name, base_class):
        if name not in item_dict:
            self.logger.error('no such %s: %s)', base_class.__name__, name)
            raise KeyError
        return func(self, item_dict, name, base_class)
    return wrapper
