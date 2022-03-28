from config.config import config
from db.mysqldb import MysqlDB
from utils import tools
from utils.log import log

db = MysqlDB(**config.get('mysqldb'))


def saveDemo(jsonstr: str):
    row = {}
    row['logo'] = data['logo']
    row['name'] = data['name']
    row['slogan'] = data['slogan']
    row['city'] = data['city']
    row['province'] = data['prov']
    row['create_time'] = tools.get_current_timestamp()
    row['update_time'] = tools.get_current_timestamp()

    sql = tools.make_insert_sql('demo_table', row, auto_update=False, update_columns=(
        'name', 'city', 'province', 'slogan', 'update_time', 'logo'))
    affect_count = db.add(sql)
    if affect_count > 0:
        log.info("数据更新成功:")


def findDemo():
    find_event_sql = "select * from demo_table  order by update_time desc "
    ret = db.find(find_event_sql, to_json=True)
    # ret 是个 json对象数组，每一个元素代表一行，通过ret['列名']获取值
    # 查到融资事件再写入
    if ret is not None and len(ret) > 0:
        print(ret)
