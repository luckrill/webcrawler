#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup
import html2text
from goose3 import Goose
from goose3.text import StopWordsChinese
from readability import Document

#url = "https://www.readmorejoy.com"
#url = "https://www.readmorejoy.com/about/"
url = "https://www.readmorejoy.com/2019/05/selecttoml/"
#url = "https://blog.csdn.net/mack415858775/article/details/40182187"

def testsoup(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80  Safari/537.36 QIHU 360SE'
    }
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    for li in soup.find_all("link"):
        print(li)
    print("----------------")
    for lili in soup.find_all("a"):
        #print(lili)
        print(lili.get("href"))



def testhtml2text(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80  Safari/537.36 QIHU 360SE'
    }
    r = requests.get(url, headers=headers)
    print(r.encoding)
    r.encoding = "utf-8"
    html = r.text

    #text_maker = html2text.HTML2Text()
    #text_maker.ignore_links = True
    #text_maker.bypass_tables = False
    #text = text_maker.handle(html)
    #print(text)

    soup = BeautifulSoup(html, 'lxml')
    #text = soup.get_text()
    #text = soup.find("div", attrs={'class':'post-content'}).get_text()
    print(soup.find("div", attrs={'class':'post-content'}))

    #'a',attrs={'id':'link1'
    #<div class="post-toc" 
    #print(soup.prettify())
    #print(text)
    #mdtext = html2text.html2text(text)
    #h = html2text.HTML2Text()
    #h.ignore_links = True
    #text = h.handle(html)
    #print(text)

def goose3text(url):
    #g = Goose()
    g = Goose({'stopwords_class': StopWordsChinese})
    article = g.extract(url=url)
    #print(article.title)
    #print(article.meta_description)
    print(article.cleaned_text)
    print("......")
    #print(article.raw_html)
    print(article.infos)

    #text = html2text.html2text(article.cleaned_text)
    
    #print(text)
    pass
    #print(utils.clean_url("http://www.abc.com#"))

#url = "https://hoxis.github.io/run-ansible-without-specifying-the-inventory-but-the-host-directly.html"
def abc(url):
    #url = "https://github.com/codelucas/newspaper"
    r= requests.get(url)
    r.encoding = "utf-8"
    #html = r.text
    doc = Document(r.text)
    print(doc.title())
    print(doc.summary())
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.bypass_tables = False
    text = text_maker.handle(doc.summary())
    print(text)

#from breadability.readable import Article
def ggg(url):
    url = "https://github.com/codelucas/newspaper"
    doc = Article(url)
    print(doc.readable)

#testhtml2text(url)
testsoup(url)
#goose3text(url)
#abc(url)
#ggg(url)

