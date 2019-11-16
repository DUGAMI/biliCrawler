# biliCrawler

### 使用方法

- 首先将cookie换为你自己的cookie，你需要首先登陆你的bilibili账号，然后随便进入一个bilibili的页面，如果是Chorme那么按F12进入抓包页面，随便打开一个包应该都能找到你的cookie，将找到的cookie复制进程序里的cookie变量

- 如果还没装selenium就pip install一下，然后把chromedriver加入path（经测试不加也可以）。测试时会自动打开chrome浏览器。

- crawl模式可以爬取指定av号的弹幕，split模式可以按你想要的秒数来分割弹幕文件，方便进行高光分析或者情感分析等
``` 
python bilibili.py crawl -i [av号(不需要av)] -o [弹幕文件路径.csv]
python bilibili.py split -i [输入文件.csv] -o [输出文件.csv] -g [分割粒度]
```

### 目前问题
- 爬取出的弹幕数量和bilibili页面显示的页面不符，使用api爬取指定日期的弹幕实际上得到的还有其他日期的弹幕，我猜测是B站为了观看体验还会混合其他日期的弹幕，目前的处理办法是去除指定日期以外的弹幕

- 爬取速度太慢，这个爬虫的逻辑是先遍历视频的发布月到当前月的所有有弹幕的日期，每次访问的时间可调，目前设定为1秒。目前想到的方法就是多线程/多进程，可能用scrapy框架更方便；此外文件写入时，如果数据量很大要考虑分块写入（还不知道云服务器什么情况）

- 扩展属性值以后有hash用户id，需要反解析出用户id(目前没有合适的反hash工具，并且也没有其他的途径获取id，暂时放弃这项)

- 现在获得的电影url是形如https://www.bilibili.com/bangumi/play/ss28872这样的，没有包含aid和cid，需要从html页面中进一步提取cid

### 参考
- [api](https://github.com/DUGAMI/biliCrawler/blob/master/api.md)的介绍

- https://blog.csdn.net/enderman_xiaohei/article/details/86659064
