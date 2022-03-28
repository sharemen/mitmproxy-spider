from typing import Sequence

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster
from config.config import config, IP
from utils.IPProxy import getProxy

ip = IP
port = config.get('spider').get('service_port')
iproxy_enable = config.get('spider').get('proxy_ip').get('enable')
proxy_user = config.get('spider').get('proxy_ip').get('proxy_user')
proxy_pass = config.get('spider').get('proxy_ip').get('proxy_pass')

http2_enable = True
if config.get('spider').get('random_ua').get('enable') == 1:
    print("======== 动态随机UA开启，需要关闭http2.0支持，自动设置 mitmprosy http2=False")
    http2_enable = False

options = Options(listen_port=port, http2=http2_enable)
dumpMaster = DumpMaster(options, with_termlog=True, with_dumper=False)

if config.get('spider').get('proxy_ip').get('enable') == 1:
    print("======== 二级代理模式开启")
    proxyip = getProxy()

    if proxyip is not None and proxyip != '':
        print("======== 成功获取到代理host: " + proxyip)
        dumpMaster.options.add_option("mode", str, "upstream:" + proxyip, "")
        dumpMaster.options.add_option("upstream_auth", str, proxy_user + ":" + proxy_pass, "")
        # dumpMaster.options.add_option("connection_strategy", str, "lazy", "")
    else:
        print("======== 没有获取到代理host，取消开启二级代理")

    # print("======" + str(dumpMaster.options))

