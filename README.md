
# 基于mitmproxy的抓取代理服务
本项目只包含代理部分，需要自己做响应内容的解析，持久化部分的开发  
启动项目，并通过将浏览器（也可以是其他工具比如selenium）的代理服务器设置为代理服务启动ip与监听端口，就可以拦截到响应内容  
之后便根据内容做各种处理，可以通过修改代码，来限定只拦截某个域名或某个url的请求响应内容:  
``` 
def response(self, flow: mitmproxy.http.HTTPFlow):

        url = flow.request.url
        if 'xxxx' in url:
            do something
```
本项目包含mysql操作工具包，具体使用可以参考项目中的demo  
本项目包含了对配置文件的解析，引用，具体使用可以参考项目中的config类  

## `一、 `支持特性
### `1.` 支持配置二级代理获取动态IP
```
proxy_ip: #动态ip代理配置
    enable: 0 #是否启用动态ip代理 0不启用,1启用
      url: #获取代理地址的url，默认支持txt格式即 ip:端口+换行
      proxy_user: 代理接口basic认证:用户名
      proxy_pass: 代理接口basic认证:密码
      reload_time: 60 #重新申请ip的时间，单位：S
```
### `2.` 支持动态更换UA，基于Fake_useragent
```
  random_ua:
    enable: 0   #是否启用随机usr-agent 基于fake-useragent
    reload_time: 60 #每个ure-agent的有效期 单位：S
```

### `3.` 支持mysql持久化（需要自行写持久逻辑，工程包含了依赖库与mysql工具类）

### `4.` 支持配置化，工程包含了依赖库与配置文件（yaml格式）

## `二、`使用说明
### `1.`启动服务
运行run_spider.py启动代理服务
会根据配置文件中的配置的端口启动代理监听  
```
spider:
  service_port: 9527 # 服务的端口
```
 
### `2.`客户端配置信任证书
客户端需要安装，并信任mitmproxy的https证书 ，才可以通过代理访问https的网址  
在启动代理服务后，会自动生成mitmproxy的证书，然后复制访问目标网站的设备上，并设置证书信任  
可以参考：https://blog.csdn.net/wywinstonwy/article/details/106541373  

### `3.`拦截response  
这里需要根据mitmproxy的框架要求开发自己的拦截插件  
可以参考capture.DemoCapture.py  
主要通过response方法拦截响应内容做解析入库的处理（需要自行开发）  
---
推荐通过 capture将 response.text -> parser类处理得数据对象data -> servce 进行持久化
的分层处理模式来进行抓取数据处理   
---
然后将开发好的XXXCapture，通过修改run_spider代码，添加到处理链中，如下所示  
可以添加多个，按顺序处理，但同一个url最好只在一个capture中处理  
```
def start():
    print("温馨提示：服务IP {} 端口 {} 请确保代理已配置".format(ip, port))

    demoaddon = DemoCapture()

    dumpMaster.addons.add(
        demoaddon
    )
    dumpMaster.run()
```
### `4.`mysql处理(引用的其他作者开源工具)
通过MysqlDB工具类，支持添加，修改、查询基本操作  
具体使用可参考：services.DemoService.py  

### `5.`配置信息处理(引用的其他作者开源工具)
可以参考config.config.py
