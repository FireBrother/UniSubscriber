# coding=utf-8
from getpass import getpass

from Announcers.MailAnnouncer import MailAnnouncer
from Master import SubscriberMaster
from Monitors.ThreeDMMonitor import ThreeDMMonitor
from Monitors.TransRushMonitor import TransRushMonitor

if __name__ == '__main__':
    # tdm = ThreeDMMonitor('闪轨2汉化帖', 'http://bbs.3dmgame.com/thread-5703118-1-1.html')
    trm = TransRushMonitor('四方-switch', '13124780166', getpass(), 'DD180221027831')
    ma1 = MailAnnouncer('ma1', 'smtp.qq.com', '417462933@qq.com', getpass(), ['417462933@qq.com'])
    # ma2 = MailAnnouncer('ma2', 'smtp.qq.com', '417462933@qq.com', getpass(), ['yangjiachen.pku@gmail.com'])
    master = SubscriberMaster('sm1')

    master.add_announcer(ma1)
    # master.add_announcer(ma2)
    master.add_monitor(trm)
    master.start()
    master.join()
