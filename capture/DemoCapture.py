import mitmproxy
from mitmproxy import ctx

from config.config import config
from parsers.DemoParser import parseData4html
from services.DemoService import saveDemo
from utils.IPProxy import set_upstream_proxy
from utils.UAutils import getRandomUA

proxy_ip_enable = False
random_ua_enable = False

class DemoCapture:

    def __init__(self):
        self.num = 0
        global proxy_ip_enable
        global random_ua_enable

        if config.get('spider').get('proxy_ip').get('enable') == 1:
            proxy_ip_enable = True

        if config.get('spider').get('random_ua').get('enable') == 1:
            random_ua_enable = True

    '''
    拦截处理header
    '''

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        """ 是否启用动态UA """
        if random_ua_enable:
            ua_reload_time = config.get('spider').get('random_ua').get('reload_time')
            flow.request.headers['User-Agent'] = getRandomUA(ua_reload_time)

    '''
    拦截请求
    '''

    def request(self, flow: mitmproxy.http.HTTPFlow):

        if flow.request.method == "CONNECT":
            return

        # 开启上游代理时才需要，更新上游代理的地址
        if proxy_ip_enable:
            set_upstream_proxy(flow, ctx)

    '''
    拦截响应
    '''

    def response(self, flow: mitmproxy.http.HTTPFlow):

        url = flow.request.url
        #if 'xxxx' in url:
        #    拦截特定url
        print(flow.response.text)
        data = parseData4html(flow.response.text)
        saveDemo(data)
        self.num = self.num + 1
        # log.info("We've seen %d flows" % self.num)

