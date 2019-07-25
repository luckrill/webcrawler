#!/usr/bin/env python3
import sys
from spider import Spider

HELPMSG = ("----------------- Usage ----------------\n"
           "1. Crawl a website:\n"
           "    python crawler.py [target_website]\n"
           "2. Help:\n"
           "    python crawler.py\n"
           "----------------------------------------\n")


def print_help():
    print("----------------------------------------")
    print("Welcome to this web crawler by Jiang Zhixiang\n")
    print(HELPMSG)

def main():
    url = "https://www.readmorejoy.com"

    args = sys.argv[0:]

    # Execute function depending on arguments
    # print(len(args))
    if len(args) == 1:
        print_help()
    elif len(args) == 2:
        url = args[1]
        #print(url)
        print("start a web crawling")
        spider = Spider(url)
        spider.crawl(url)
        print("web crawling done")
    else:
        print_help()


if __name__ == "__main__":
    main()