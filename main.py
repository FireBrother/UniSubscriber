# coding=utf-8
from getpass import getpass

from Announcers.MailAnnouncer import MailAnnouncer
from Master import SubscriberMaster
from Monitors.ThreeDMMonitor import ThreeDMMonitor

if __name__ == '__main__':
    tdm = ThreeDMMonitor('闪轨2汉化帖', 'http://bbs.3dmgame.com/thread-5703118-1-1.html')
    ma1 = MailAnnouncer('ma1', 'smtp.qq.com', '417462933@qq.com', '7766Andy', ['417462933@qq.com'])
    ma2 = MailAnnouncer('ma2', 'smtp.qq.com', '417462933@qq.com', '7766Andy', ['yangjiachen.pku@gmail.com'])
    master = SubscriberMaster('sm1')

    master.add_announcer(ma1)
    master.add_announcer(ma2)
    master.add_monitor(tdm)
    master.start()
    master.join()
