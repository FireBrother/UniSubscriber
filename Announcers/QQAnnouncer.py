# coding=utf-8
import atexit
import code
import os
from time import sleep

import subprocess

from Announcer import BaseAnnouncer


@atexit.register
def stop_qqbot():
    os.system('qq stop')


class QQAnnouncer(BaseAnnouncer):
    def __init__(self, name, qq, target_qq, **kwargs):
        super(QQAnnouncer, self).__init__(name, **kwargs)
        self.qq = qq
        self.target_qq = target_qq
        self.qqbot = subprocess.Popen(['qqbot', '-q', qq], stdout=subprocess.PIPE)
        while True:
            out = self.qqbot.stdout.readline()
            print out.strip()
            if '登录成功。' in out:
                break

    def announce(self, msg):
        for tq in self.target_qq:
            text = 'From: {}\\\\n{}'.format(msg[0], msg[1]['msg'])
            os.system('qq send buddy {} {}'.format(tq, text))
            print text


if __name__ == '__main__':
    qqa = QQAnnouncer('qq', '1782167414', ['417462933'])
    # qqa.announce('123')
