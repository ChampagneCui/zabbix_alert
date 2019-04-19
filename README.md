# zabbix_alert
zabbix钉钉告警有图版

![Aaron Swartz](https://github.com/ChampagneCui/zabbix_alert/blob/master/warning.png)

本应用旨在zabbix钉钉告警时附上相关监控图，使得告警更加清晰

采用的图床是阿里云的oss，其他图床请自行改写

网上看了各种有图版告警，都是用类似于curl导出的方式来导出告警图片的，我的这个是更加粗暴的浏览器截图，好处是理论上可以配合任何监控图表，后续可能会考虑出grafana版本


环境：

python3.6 

centos6.8 (ps:centos7更推荐)

phantomjs

安装依赖：
```
#sudo pip install oss2
#sudo pip install selenium
#sudo pip install dingtalkchatbot
```
下载
```
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
```
解压后放到/opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs

###说下我为什么更推荐centos7的原因：
你们如果读源代码会发现我现在用的是selenium.PhantomJS，selenium其实是可以配合firefox和chrome的，我试了firefox版本，有各种bug，网上查到说selenium配合firefox没有chrome好。
然而谷歌已经放弃了对centos6安装chrome的适配，所以我只能选用PhantomJS，有心的人可以把我截图功能的那段在centos7上用chrome改写一下。

另外钉钉本身是不支持直接发送图片的，所以我这里选用的是发送markdown格式

zabbix里设置告警的message：
```
{
'告警主机':'{HOST.NAME}',
'告警地址':'{HOST.IP}',
'监控项目':'{ITEM.NAME}',
'监控项ID':{ITEM.ID},
'监控取值':'{ITEM.LASTVALUE}',
'告警等级':'{TRIGGER.SEVERITY}',
'当前状态':'{TRIGGER.STATUS}',
'告警信息':'{TRIGGER.NAME}',
'告警时间':'{EVENT.DATE} {EVENT.TIME}'
}
```
上面的其他项随便你改，监控项ID是关键，我用这个id去last data里取图片的
