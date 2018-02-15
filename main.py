# coding=utf-8
from getpass import getpass

from Announcers.MailAnnouncer import MailAnnouncer
from Master import SubscriberMaster
from Monitors.ThreeDMMonitor import ThreeDMMonitor

if __name__ == '__main__':
    tdm = ThreeDMMonitor('闪轨2汉化帖', 'http://bbs.3dmgame.com/thread-5703118-1-1.html')
    ma = MailAnnouncer('ma', 'smtp.qq.com', '417462933@qq.com', getpass(), ['417462933@qq.com'])
    master = SubscriberMaster('sm1')

    master.add_announcer(ma)
    master.add_monitor(tdm)
    master.start()
    master.join()
