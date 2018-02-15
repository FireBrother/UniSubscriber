# coding=utf-8
import os
import smtplib
import subprocess
from email.header import Header
from email.mime.text import MIMEText
from getpass import getpass

from Announcer import BaseAnnouncer


class MailAnnouncer(BaseAnnouncer):
    def __init__(self, name, mail_host, username, passwd, receivers, **kwargs):
        super(MailAnnouncer, self).__init__(name, **kwargs)
        self.mail_host = mail_host
        self.username = username
        self.passwd = passwd
        self.receivers = receivers

    def announce(self, msg):
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(self.mail_host, 465)  # 25 为 SMTP 端口号
        smtpObj.login(self.username, self.passwd)

        message = MIMEText(msg[1]['msg'], 'plain', 'utf-8')
        message['From'] = Header('MailAnnouncer#{}#{}'.format(self.name, msg[0]), 'utf-8')
        message['To'] = Header('订阅者', 'utf-8')
        message['Subject'] = Header('UniSubscriber#'+msg[0], 'utf-8')

        smtpObj.sendmail(self.username, self.receivers, message.as_string())


if __name__ == '__main__':
    ma = MailAnnouncer('ma', 'smtp.qq.com', '417462933@qq.com', getpass(), ['417462933@qq.com'])
    msg = []
    msg.append('test')
    msg.append({'msg': 'message'})
    ma.announce(msg)
