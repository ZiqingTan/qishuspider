
"""
只爬了从小说类型青春到经管，后面的基本上都是重复的了，如果后面的全本啊，排行啊什么的，直接在函数parse_url下的for url in index_url_list[1:-4]，直接
改为or url in index_url_list就可以了

"""
from fake_useragent import UserAgent #fake_useragent需要安装 直接打开输入命令pip install fake_useragent
import requests
from pyquery import PyQuery as pq
import re
import os
index_url_list = []
title_list = []

def request_url(url):
    headers = {"User-Agent": UserAgent().random, }
    response = requests.get(url, headers=headers)
    return response
def spider_code():
    headers = {"User-Agent":UserAgent().random,}
    response = request_url("https://m.bookbao99.net/")
    if response.status_code == 200:
        doc = pq(response.text)
        index_url = doc(".am-g .am-nav li a").items()
        for i in index_url:
            index_url_list.append("https://m.bookbao99.net" + i.attr("href")[:9]+"-p_{}"+i.attr("href")[9:])
            title_list.append(i.text())

def parse_url():
    count = 1
    for url in index_url_list[1:-4]:
        print("正在爬取",title_list[count])
        #拼接小说的页数
        response = request_url(url.format(1))
        res = re.compile('\(第1/(.*?)页\)当前26条/页')
        number = re.search(res, response.text)
        #print(number.group(1),count)
        for i in range(0,int(number.group(1))):#拼接的页数
            response_1 = request_url(url.format(i))
            if response_1.status_code == 200:
                doc = pq(response_1.text)
                url_children = doc(".am-list-news .am-list-news-bd .am-list .am-g a").items()
                #请求小说url
                for i in url_children:
                    response_2 = request_url("https://m.bookbao99.net" + i.attr("href"))
                    if response_2.status_code == 200:
                        #获取下载书籍的地址
                        docs1 = pq(response_2.text)
                        download = docs1(".am-list-news .am-list-news-bd .am-list .am-list-item-desced .am-list-main h3 a").text()
                        res = re.compile('<a href="(.*?)">下载书籍</a>')
                        url_download_s = re.search(res, response_2.text)
                        response_3 = request_url("https://m.bookbao99.net" + url_download_s.group(1))
                        if response_3.status_code == 200:
                            #获取小说下载地址
                            resp = re.compile('<a href="(.*?)">.*?下载1')
                            download_url_one = re.search(resp, response_3.text)
                            print("正在下载",download)
                            #写入文件
                            parse_url_item(title_list[count], download,download_url_one.group(1))
                            print( download,"下载完成")
        count += 1
def parse_url_item(indx,title,url):
    #创建文件夹
    if not os.path.exists(indx):
        os.mkdir(indx)
    file_path = '{0}/{1}.{2}'.format(indx,title,"txt")
    response = request_url(url)
    if response.status_code == 200:
        #文件不存在则创建
        if not os.path.exists(file_path):
            with open(file_path,'wb') as f:
                f.write(response.content)
        else:
            #别担心有重复的，已经判断了
            pass

if __name__ == "__main__":
    spider_code()
    parse_url()