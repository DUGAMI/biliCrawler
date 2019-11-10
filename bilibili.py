# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import argparse

import re
import time
from datetime import timedelta,datetime
from calendar import monthrange

from selenium import webdriver
import time


def write_down(html, filename='test.html'):
    with open(filename, 'w') as f:
        f.write(html)


header = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
}

#把cookie换成自己的
cookie="l=v; CURRENT_FNVAL=16; _uuid=94B3C680-96DA-07D9-BB7E-D5CE95B425AD74983infoc; buvid3=3F53EC9D-3A06-478F-AAA5-49F23215E5C5155825infoc; LIVE_BUVID=AUTO5515684319449519; sid=8am1lxji; stardustvideo=1; rpdid=|(umJuk||uJk0J'ulY)RJumml; laboratory=1-1; im_notify_type_6068608=0; UM_distinctid=16dabd48276753-0b7744c22fbdb3-67e1b3f-a5aa4-16dabd4827742b; DedeUserID=6068608; DedeUserID__ckMd5=ff0837eb05d5b330; SESSDATA=784365e7%2C1573918720%2Ca433daa1; bili_jct=70b505c5084e7816170d362b7865e922; stardustpgcv=0606; CURRENT_QUALITY=64"
cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}

#每次访问后停留的秒数
waitingTime = 1

def get_danmuku(cid, filename, dateList):

    fw=open(filename,"w",encoding="utf-8")

    danmuku_api = "https://api.bilibili.com/x/v2/dm/history?type=1&oid={}&date={}"

    print(u"写入弹幕ing...")
    count_danmu = 0 #计数器
    for idx,date in enumerate(dateList):
        print("弹幕日期{} [{}/{}]".format(date,idx+1,len(dateList)))
        r2 = requests.get(danmuku_api.format(cid,date), headers=header,cookies=cookie_dict)
        soup = BeautifulSoup(r2.content, 'lxml')
        danmus = soup.find_all('d')
        # print(danmus[0])

        for danmu in danmus:
            content = danmu.string
            attr = danmu['p'].split(',')
            video_position = str(attr[0])  # 弹幕位于视频中的时间点，以秒数为单位
            post_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(attr[4])))  # 弹幕发布的日期时间，由UNIX转换为字符串
            user_id_hash = attr[6] # 经过Hash的用户id
            danmu_id = attr[7] # 弹幕在数据库中的id

            #将非当天发送的弹幕去除（为了观看体验，B站会把当天发送的弹幕和历史弹幕以一定比例混合）
            
            temp=time.strftime('%Y-%m-%d', time.localtime(int(attr[4])))
            if temp!=date:
                continue
            
            # timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t2)))
            fw.write(content+'\t'+video_position+'\t'+post_datetime+'\t'+danmu_id+'\t'+user_id_hash+'\n')
            count_danmu += 1
        time.sleep(waitingTime)

    fw.close()
    print(u"共写入%d条弹幕...请查看"%(count_danmu) + filename)


#获取该程序需要的视频基本信息（cid号、投稿时间）
def get_basicInfo(aid):

    basicInfo={}
    #videoInfo = "https://bangumi.bilibili.com/player/web_api/v2/playurl=" + url_test
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
        #print(index)
        time.sleep(waitingTime)
        
        if index["data"]==None:
            postTime = postTime + delta
            continue

        for dd in index["data"]:
            date_list.append(dd)

        postTime = postTime + delta
        

    return date_list

def get_movie_url(start_url, page=1):
    '''通过start_url的电影索引页获取页面所有电影的播放页面链接
    Args:
        start_url:一般设置为电影目录的第一页
        page:需要爬取的页数，默认为1
    Returns:
        url_list: url列表
        name_list: 电影名称列表，两个列表对应
    '''
    # 实例化一个浏览器
    driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    current_url = start_url
    url_list = []
    name_list = []
    for i in range(page):
        print('正在爬取第%d页'%(i+1))
        driver.get(current_url)
        item_list = driver.find_elements_by_xpath("//li[@class='bangumi-item']/a[@class='bangumi-title']")
        for item in item_list:
            url = item.get_attribute("href")
            movie_name = item.text
            print(movie_name)
            url_list.append(url)
            name_list.append(movie_name)
        time.sleep(1)
        # 下一页
        driver.find_element_by_xpath("//a[@class='p next-page']").click()
        current_url = driver.current_url
    # 退出浏览器
    driver.quit()
    return url_list, name_list


def main():

    aid,filename=get_input_id()
    basicInfo = get_basicInfo(aid)
    res = get_date(basicInfo["cid"], basicInfo["time"])
    get_danmuku(basicInfo["cid"], filename, res)

    #获取电影url和电影名列表（还没有和爬取弹幕结合），page设置爬取页数
    start_url = 'https://www.bilibili.com/movie/index/#st=2&order=2&area=-1&style_id=-1&release_date=-1&season_status=-1&sort=0&page=1'
    url_list, name_list = get_movie_url(start_url, page=2)
    #print(url_list)
    #print(name_list)


if __name__ == '__main__':
    main()
