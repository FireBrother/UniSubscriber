# coding=utf-8
import re
import requests

from bs4 import BeautifulSoup
import getpass

from Monitor import BaseMonitor


class TransRushMonitor(BaseMonitor):
    def __init__(self, name, uid, passwd, orderId, **kwargs):
        super(TransRushMonitor, self).__init__(name, **kwargs)
        self.uid = uid
        self.passwd = passwd
        self.orderId = orderId

    def diff(self, prev_content, now_content):
        return set(now_content).difference(set(prev_content))

    def extract_content(self):
        s = requests.session()
        s.get('http://passport.transrush.com/AjaxPassport.aspx?time=1520138241391&actionType=0&pwd={}&email={}'
                  '&isRememberPwd=false&ref=http%3A%2F%2Fmember.transrush.com%2FMember%2FMyParcel.aspx'
                  '&_=1520138227057'.format(self.passwd, self.uid))
        r = s.get('http://member.transrush.com/Member/parcelDetail.aspx?fromTab=sy&orderNo={}'
                  '&toTab=trace'.format(self.orderId))
        bs = BeautifulSoup(r.text, 'html.parser')
        table = bs.select('#trace > table')
        trs = table[0].find_all('tr')
        content = []
        for tr in trs[1:]:
            tds = tr.find_all('td')
            content.append(tuple(map(lambda x: x.text.strip(), tds)))
        return content

    def gen_msg(self):
        msg = dict()
        msg['msg'] = '<br \>'.join(map(lambda x: ':'.join(x), self.diff_content)).encode('utf8')
        msg['status'] = 0
        return msg


if __name__ == '__main__':
    trm = TransRushMonitor('四方-switch', '13124780166', getpass.getpass(), 'DD180221027831')
    trm.now_content = trm.extract_content()
    trm.prev_content = ['123']
    trm.diff_content = trm.diff(trm.prev_content, trm.now_content)
    print(trm.gen_msg())
