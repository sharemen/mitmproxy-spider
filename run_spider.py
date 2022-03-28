# -*- coding: utf-8 -*-
"""
Created on 2019/5/18 9:52 PM
---------
@summary:
---------
@author:
"""



from DumpMaster import dumpMaster, ip, port
from capture.DemoCapture import DemoCapture
from capture.ItjuzCapture import ItjuzCapture


def start():
    print("温馨提示：服务IP {} 端口 {} 请确保代理已配置".format(ip, port))

    itjuzaddon = ItjuzCapture()
    #demaoaddon = DemoCapture()

    dumpMaster.addons.add(
        itjuzaddon
        #, demaoaddon
    )
    dumpMaster.run()


def main():
    start()


if __name__ == '__main__':
    main()
