# biliCrawler

### 使用方法

- 首先将cookie换为你自己的cookie，你需要首先登陆你的bilibili账号，然后随便进入一个bilibili的页面，如果是Chorme那么按F12进入抓包页面，随便打开一个包应该都能找到你的cookie，将找到的cookie复制进程序里的cookie变量

- 使用``` python bilibili.py -i [av号(不需要av)] -o [弹幕文件路径.csv]```运行该程序

### 目前问题
- 爬取出的弹幕数量和bilibili页面显示的页面不符，使用api爬取指定日期的弹幕实际上得到的还有其他日期的弹幕，我猜测是B站为了观看体验还会混合其他日期的弹幕，目前的处理办法是去除指定日期以外的弹幕

- 爬取速度太慢，这个爬虫的逻辑是先遍历视频的发布月到当前月的所有有弹幕的日期，每访问一个月会停留2s，然后实际爬弹幕时是一天一天爬的，以你的名字这个视频为例，假设它有800天都有弹幕，那么爬取大概需要1600s

- 还有爬取用户信息的问题没有解决

[api](https://github.com/DUGAMI/biliCrawler/blob/master/api.md)的介绍
