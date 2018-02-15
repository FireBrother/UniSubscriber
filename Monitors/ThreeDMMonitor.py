# coding=utf-8
import re
import requests

from Monitor import BaseMonitor


class ThreeDMMonitor(BaseMonitor):
    def __init__(self, name, url, **kwargs):
        super(ThreeDMMonitor, self).__init__(name, **kwargs)
        self.url = url

    def diff(self, prev_content, now_content):
        return set(now_content).difference(set(prev_content))

    def extract_content(self):
        ret = requests.get(self.url)
        title = re.search('<title>(.*)</title>', ret.text)
        return title.group(1)

    def gen_msg(self):
        msg = dict()
        msg['msg'] = '标题更新：{}'.format(self.now_content)
        msg['status'] = 0
        return msg


if __name__ == '__main__':
    tdm = ThreeDMMonitor('闪轨2汉化帖', 'http://bbs.3dmgame.com/thread-5703118-1-1.html')
    tdm.extract_content()
