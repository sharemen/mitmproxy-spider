from urllib.parse import urlparse

import requests as requests
import mitmproxy
from mitmproxy.net.server_spec import ServerSpec
from mitmproxy import ctx

from config.config import config
from utils import tools

ipproxy_enable = False
get_proxy_url = ''
rtime = 30
proxy_list = []
validtime = 0
proxyindex = 0

if config.get('spider').get('proxy_ip').get('enable') == 1:

    ipproxy_enable = True
    get_proxy_url = config.get('spider').get('proxy_ip').get('url')
    if config.get('spider').get('proxy_ip').get('reload_time') is not None and str.isnumeric(
            str(config.get('spider').get('proxy_ip').get('reload_time'))):
        rtime = config.get('spider').get('proxy_ip').get('reload_time')

    norepeat = config.get('spider').get('proxy_ip').get('norepeat')
    other = config.get('spider').get('proxy_ip').get('other')


def getHost(url: str) -> str:
    parsed_uri = urlparse(url)
    host = '{host.netloc}'.format(probuf=parsed_uri, host=parsed_uri)
    return host


def getProxy():
    global validtime
    global proxy_list
    global proxyindex

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Host': getHost(get_proxy_url),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
    }

    proxies = {
        "http": None,
        "https": None,
    }

    if get_proxy_url == '':
        return ''

    else:
        # 可用代理列表为空
        if len(proxy_list) == 0:

            # 获取代理信息时，采取直连，忽略系统代理

            print("==== request get_proxy_url:" + get_proxy_url)
            proxy_req = requests.get(get_proxy_url, headers=headers, proxies=proxies)
            # print("==== get_proxy_url reponse: " + proxy_req.text)
            req_text_arr = proxy_req.text.split("\r\n")

            for proxyip in req_text_arr:
                if proxyip != '':
                    proxy_list.append(proxyip)

            # 保险起见，按照声明有效期的60%来更新代理列表，例如配置150S 有效期
            # 如果当前已经达到 150S*0.8 = 120S 就更新代理列表
            validtime = tools.get_current_timestamp() + rtime
        # 代理有效期超期
        elif tools.get_current_timestamp() > validtime:
            proxy_list.clear()
            proxy_req = requests.get(get_proxy_url, headers=headers, proxies=proxies)
            # print("==== renew get_proxy_url reponse: " + proxy_req.text)
            req_text_arr = proxy_req.text.split("\r\n")
            for proxyip in req_text_arr:
                if proxyip != '':
                    proxy_list.append(proxyip)
            validtime = tools.get_current_timestamp() + rtime

        if len(proxy_list) > 0:
            # print("==== proxy_list : " + str(proxy_list))
            ret = proxy_list[proxyindex]
            if proxyindex + 1 >= len(proxy_list):
                proxyindex = 0
            else:
                proxyindex = proxyindex + 1
            return ret
        else:
            return ''


def set_upstream_proxy(flow: mitmproxy.http.HTTPFlow, mitmctx: mitmproxy.ctx):
    proxyinfo = getProxy()
    proxy_address = (proxyinfo.split(":")[0], int(proxyinfo.split(":")[1]))

    is_proxy_change = proxy_address != flow.server_conn.via.address
    server_connection_already_open = flow.server_conn.timestamp_start is not None
    if is_proxy_change and server_connection_already_open:
        # server_conn already refers to an existing connection (which cannot be modified),
        # so we need to replace it with a new server connection object.
        # flow.server_conn = Server(flow.server_conn.address)
        "已经打开的链接不更换代理"

    if is_proxy_change:
        print("原代理" + str(flow.server_conn.via.address) + '|新代理' + str(proxy_address))
        flow.server_conn.via = ServerSpec('http', proxy_address)

        mode_option = {'mode': str('upstream:' + proxyinfo)}
        # 更新运行环境中的代理设置
        # print("当前运行环境代理配置：" + ctx.master.options.__getattr__('mode'))
        mitmctx.master.options.update(**mode_option)
        # print("当前运行环境配置更新后：" + ctx.master.options.__getattr__('mode'))
