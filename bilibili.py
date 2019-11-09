# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import argparse

import re
import time
from datetime import timedelta,datetime
from calendar import monthrange


def write_down(html, filename='test.html'):
    with open(filename, 'w') as f:
        f.write(html)


header = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
}

#记得吧cookie换成自己的
cookie=""
cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}

#每次访问后停留的秒数
waitingTime=2

def get_danmuku(cid, filename,dateList):

    fw=open(filename,"w",encoding="utf-8")

    danmuku_api = "https://api.bilibili.com/x/v2/dm/history?type=1&oid={}&date={}"

    print(u"写入弹幕ing...")

    for idx,date in enumerate(dateList):
        print("弹幕日期{} [{}/{}]".format(date,idx+1,len(dateList)))
        r2 = requests.get(danmuku_api.format(cid,date), headers=header,cookies=cookie_dict)
        soup = BeautifulSoup(r2.content, 'lxml')
        danmus = soup.find_all('d')

        for danmu in danmus:
            content = danmu.string
            attr = danmu['p'].split(',')
            t1 = str(attr[0])  # 视频中的时间
            t2 = attr[4]  # 发布时间

            #将非当天发送的弹幕去除（为了观看体验，B站会把当天发送的弹幕和历史弹幕以一定比例混合）
            temp=time.strftime('%Y-%m-%d', time.localtime(float(t2)))
            if temp!=date:
                continue

            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t2)))
            fw.write(content + ',' + t1 + ',' + timestr + '\n')
        time.sleep(waitingTime)

    fw.close()
    print(u"写入完成...请查看" + filename)


#获取该程序需要的视频基本信息（cid号、投稿时间）
def get_basicInfo(aid):

    basicInfo={}

    videoInfo = "https://api.bilibili.com/x/web-interface/view?aid=" + aid
    videoInfoJson = requests.get(videoInfo,cookies=cookie_dict).json()
    postTime = time.localtime(videoInfoJson["data"]["ctime"])
    postTime = datetime(postTime.tm_year, postTime.tm_mon, postTime.tm_mday)

    cid=videoInfoJson["data"]["cid"]

    basicInfo["time"]=postTime
    basicInfo["cid"]=cid

    return basicInfo

#命令行信息处理
def get_input_id():
    parser = argparse.ArgumentParser(description='Welcome to BILI')
    parser.add_argument('-i', '--input', help='set the av_number to crawl')
    parser.add_argument('-o', '--output', help='set the filename to store')
    args = parser.parse_args()
    if args.output:
        filename = args.output
    else:
        filename = 'test.csv'
    aid = str(args.input)

    return (aid,filename)

#获取爬取视频的所有有弹幕的日期
def get_date(cid,postTime):
    date_index="https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={}&month={}"

    date_list=[]

    #获取当月最后一天
    now=datetime.now()
    lastDay=monthrange(now.year,now.month)[1]
    lastDay=datetime(now.year,now.month,lastDay)

    while postTime<=lastDay:
        delta = timedelta(days=monthrange(postTime.year,postTime.month)[1])
        d=postTime.strftime("%Y-%m")
        index=requests.get(date_index.format(cid,d),cookies=cookie_dict).json()
        #print(d)

        time.sleep(waitingTime)
        if index["data"]==None:
            postTime = postTime + delta
            continue

        for dd in index["data"]:
            date_list.append(dd)

        postTime = postTime + delta

    return date_list

def main():

    aid,filename=get_input_id()
    basicInfo = get_basicInfo(aid)
    res = get_date(basicInfo["cid"], basicInfo["time"])
    get_danmuku(basicInfo["cid"], filename, res)


if __name__ == '__main__':
    main()
