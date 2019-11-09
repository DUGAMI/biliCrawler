# 该程序用到的api

### 获取基本信息
https://api.bilibili.com/x/web-interface/view?aid=xxx
xxx是指视频的av号，aid都是指av号，访问后会返回一个json格式的文件，目前只用到了cid和ctime这两个信息

### 获取指定视频指定月份的有弹幕的日期
https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={}&month={}
oid是指cid，月份用xx年-xx月的格式

### 获取指定视频指定日期的弹幕
https://api.bilibili.com/x/v2/dm/history?type=1&oid={}&date={}
oid是指cid，date用xx年-xx月-xx日的格式