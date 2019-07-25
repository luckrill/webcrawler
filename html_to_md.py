#!/usr/bin/env python3
# This file
# Author: Jiang Zhixiang
# Date: 06/18/2019

import requests
from bs4 import BeautifulSoup
import html2text
from readability import Document
from goose3 import Goose
from goose3.text import StopWordsChinese
import time
import argparse
from selenium import webdriver

urlparse = ""
count = 0

def html_to_md(url=None, html=None, type=None):
    global count
    print(url)
    print(type)
    if (html == None) and (type == None):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80  Safari/537.36 QIHU 360SE'
        }
        r = requests.get(url, headers=headers)
        # r = requests.get(url, headers=headers, verify=False)
        print(r.encoding)
        #r.encoding = r.apparent_encoding
        #r.encoding = "utf-8"
        html = r.text
        #print(r.text)
        soup = BeautifulSoup(html, 'lxml')
    elif (html == None) and (type != None):
        # select one, I think PhantomJS is fast and enough
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver = webdriver.Chrome()

        driver = webdriver.PhantomJS()

        driver.get(url)
        driver.implicitly_wait(5)

        html = driver.page_source

        soup = BeautifulSoup(html, 'lxml')
        driver.close()

    else:
        soup = BeautifulSoup(html, 'lxml')

    # which one
    # weixin
    #select_html = soup.find("div", attrs={'class':'rich_media_content'})
    # zhihu
    #select_html = soup.find("div", attrs={'class':'Post-RichTextContainer'})
    # cn blogs
    #select_html = soup.find("div", attrs={'class':'post'})

    #select_html = soup.find("article")
    #select_html = soup.find("div", attrs={'class':'row'})

    # sohu
    # runoob
    #select_html = soup.find("div", attrs={'class':'article'})
    # select_html = soup.find("div", attrs={'class':'post-content'})
    # 简书网站
    # select_html = soup.find("div", attrs={'class':'post'})
    # csdn
    select_html = soup.find("div", attrs={'class':'blog-content-box'})
    # 头条
    #select_html = soup.find("body")
    # 头条
    #select_html = soup.find("div", attrs={'class':'article-box'})
    # 知乎
    #select_html = soup.find("div", attrs={'class':'Post-content'})
    #
    #select_html = soup.find("div", attrs={'class':'section content'})
    # linux.cn
    # select_html = soup.find("div", attrs={'id':'article_content'})
    #select_html = soup.find("div", attrs={'id':'main'})
    #select_html = soup.find("div", attrs={'class':'Section1'})
    #print(select_html)
    md = html2text.html2text(str(select_html))
    print(md)

    # html_read_to_text(str(html))
    # html_goose_to_text(str(html))

    #text_maker = html2text.HTML2Text()
    #text_maker.ignore_links = True
    #text_maker.bypass_tables = False
    #md = text_maker.handle(html)
    count += 1
    timestr = time.strftime('%Y%m%d-%M', time.localtime(time.time()))  #转化为时间格式2018-12-11 12：20：20
    filename = ("md/text" + str(count).zfill(3)) + ".md"
    # print(md)
    with open(filename, "w") as f:
        f.write(md)

def html_read_to_text(html):
    doc = Document(html)
    print(doc.title())
    print(doc.summary())
    # more content info can be get

def html_goose_to_text(html):
    g = Goose({'stopwords_class': StopWordsChinese})
    # article = g.extract(url=url)
    article = g.extract(html=html)
    print(article.title)
    print(article.cleaned_text)
    # more more content info can be get

url = "https://www.yangzhiping.com/psy/Principles.html"
#url = "https://www.readmorejoy.com/about/"
#url = "https://www.readmorejoy.com/2019/05/release02/"
#blog2text(url)
#doc2text(url)

# CLI
################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=str)
    parser.add_argument('-u', type=str)
    parser.add_argument('-f', type=str)
    args = parser.parse_args()
    print(args)
    if args.u != None:
        url = args.u
        if not url.startswith("http"):
            print("please input right url!")
            exit()
        html_to_md(url, type=args.t)

    if args.f != None:
        with open(args.f) as f:
            lines = f.readlines()
            for li in lines:
                url = li.strip("\n")
                html_to_md(url, type=args.t)

    # html_to_md(url)
