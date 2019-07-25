# This file contains core classes for this simple web crawler.
# Author: Jiang Zhixiang
# Date: 06/18/2019
import requests
from urllib.parse import urljoin, urlparse        # for join two urls and parse url
from bs4 import BeautifulSoup

class Spider():
    def __init__(self, rooturl):
        self.to_visit = []
        self.visted = set([])
        self.exterLink = set([])
        rooturl = self.clean_url(rooturl)
        self.parse_result = urlparse(rooturl)
        print(self.parse_result)
        # let domain include path, for some time only need path web page
        self.domain = self.parse_result.netloc + self.parse_result.path
    
    def crawl(self, target_url):
        target_url = self.clean_url(target_url)      # clean target_url
        self.to_visit.append(target_url)    # put target_url to to_visit list
        i = 0
        while len(self.to_visit) > 0:
            url = self.to_visit.pop(0)      # get next url, pop(0) is first item
            i += 1
            print("The spider %d is visiting: %s" % (i, url))
            urls = self.parser_url(url)     # parse the url and get all urls from one html page
            self.visted.add(url)            # add this visted url to visted list

            # Add urls from the praser to to_visit lits
            # When they are not visited or already in the to_vist list
            for url in urls:
                if url not in self.visted and url not in self.to_visit:
                    self.to_visit.append(url)
        
        print("Ok, The spider has finished crawling the web at {url}".format(url=target_url))
        # print(" save inter url to results.log")
        with open("results.log", "w") as f:
            for url in self.visted:
                f.write(url + "\n")
                # print(url)
        # print("web url list exter link")
        # for url in self.exterLink:
        #     print(url)
    
    def parser_url(self, current_url):
        '''
        Parse the url and get all urls from one html page
        '''
        urls = []
        #print("execute parse_url: " + current_url)

        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80  Safari/537.36 QIHU 360SE'
        }

        try:
            r = requests.get(current_url, headers=headers) # with test, some web need headers
            if (r.status_code != 200):
                print("status_code: %d" % r.status_code)
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            
            # ******
            # can insert your parse fuction at here
            # get all you need
            #print(soup.get_text())
            # ******

            # return [x['href'] for x in parser.findAll('a') if x.has_attr('href')]
            for link in soup('a'):
                #print(link)
                get_a_url = link.get("href")
                #print(get_a_url)
                newurl = urljoin(current_url, get_a_url) # append relative path to the root path
                newurl = self.clean_url(newurl)                # clean up url
                if self.url_valid(newurl, self.domain):
                    urls.append(newurl)       # append url to the return list

        except requests.exceptions.ReadTimeout:
            print('Timeout')
        except requests.exceptions.ConnectionError:
            print('Connection error')
        except requests.exceptions.RequestException:
            print('Error')

        return urls

    def parse_html(self, html):
        # html2md orgin
        # goose3 ver
        
        pass

    def url_valid(self, url, domain):
        if url.startswith("http"):
            if domain in url:
                # maybe inter link
                #print("maybe inter link: " + url)
                return True
            else:
                # maybe exter link
                #print("maybe exter link: " + url)
                if url not in self.exterLink:
                    self.exterLink.add(url)
                return False
        return False

    def clean_url(self, url):
        '''
        Clean up url by
            - always start with "http://" or "https://"
            - remove element jumping #
            - remove last '/'
        @input:
            url     :   the url to be processed
        @output:
            url     :   the clean url
        '''
        # Deal with "http(s)://"
        if url[0:4] != "http":
            url = "http://" + url

        # Deal with "#"
        idx = url.find('#')
        if idx != -1:
            url = url[:idx]

        # Deal with last "/"
        url = url.rstrip('/')

        return url    