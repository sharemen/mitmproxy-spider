import os
import sys

import fake_useragent
from fake_useragent import UserAgent

from utils import tools

if 'python' in sys.executable:
    abs_path = lambda file: os.path.abspath(os.path.join(os.path.dirname(__file__), file))
else:
    abs_path = lambda file: os.path.abspath(
        os.path.join(os.path.dirname(sys.executable), file))  # mac 上打包后 __file__ 指定的是用户根路径，非当执行文件路径

ua: UserAgent
#优先匹配当前试用版本的UA配置
if os.path.exists(abs_path('./fake_useragent_%s.json' % fake_useragent.VERSION)):
    location = abs_path('./fake_useragent_%s.json' % fake_useragent.VERSION)
    ua = fake_useragent.UserAgent(path=location)
#其次匹配都低配置
elif os.path.exists(abs_path('./fake_useragent.json')):
    location = abs_path('./fake_useragent.json')
    ua = fake_useragent.UserAgent(path=location)
#最后使用默认
else:
    ua = UserAgent(use_cache_server=False, verify_ssl=False)

user_agent_inuse = ''
valid_time = 0

def getRandomUA(rtime: int):
    global valid_time
    global user_agent_inuse

    if ua is not None:
        if rtime is not None and rtime > 0:
            if valid_time == 0:
                user_agent_inuse = str(ua.random)
                valid_time = tools.get_current_timestamp() + rtime
                print("========= 首次生产UA:"+user_agent_inuse)
            elif tools.get_current_timestamp() > valid_time:
                user_agent_new = str(ua.random)
                print("========= 更新UA 【old】:" + user_agent_inuse)
                print("========= 更新UA 【new】:" + user_agent_new)
                user_agent_inuse = user_agent_new
                valid_time = tools.get_current_timestamp() + rtime


            return user_agent_inuse
        else:
            return str(ua.random)
    else:
        return ''
