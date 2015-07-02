#!/usr/bin/env python

#*******************************#
# Description: Hack Utils       #
# Author: avfisher#wooyun.org   #
# Email: security_alert@126.com #
#*******************************#

import urllib2
import re
import sys
import os
import time
import ssl
import getopt

from bs4 import BeautifulSoup

# Ignore SSL error when accessing a HTTPS website
ssl._create_default_https_context = ssl._create_unverified_context

reload(sys)
sys.setdefaultencoding( "gb2312" )

def logfile(log,logfile):
    f=open(logfile,'a')
    f.write(log+"\n")
    f.close

def isExisted(mystr,filepath):
    if os.path.exists(filepath):
        mystr=mystr.strip()
        f=open(filepath,'r')
        num=0
        for eachline in f:
            if mystr in eachline:
                num=num+1
            else:
                num=num
        if num >0:
            return True
        else:
            return False
    else:
        return False

def getUrlRespHtml(url):
    heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
            'Accept-Language':'zh-cn,zh;q=0.5', 
            'Cache-Control':'max-age=0', 
            'Connection':'keep-alive', 
            'Keep-Alive':'115',
            'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14'}
 
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener) 
    req = urllib2.Request(url)
    opener.addheaders = heads.items()
    respHtml = opener.open(req).read()
    return respHtml

def getLinksFromBaidu(html):  
    soup = BeautifulSoup(html)
    html=soup.find('div', id="content_left")
    if html is None:
        print '[!] failed to crawl'
    else:
        html_doc=html.find_all('h3',class_="t")
        if html_doc is None:
            print '[!] failed to crawl'
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            for doc in html_doc:
                try:
                    href=doc.find('a')
                    link=href.get('href')
                    rurl=urllib2.urlopen(link.strip()).geturl()
                    if not isExisted(rurl,'urls.txt'):
                        logfile(rurl,'urls.txt')
                        print "[+] "+rurl
                    else:
                        print "[!] url is duplicate ["+rurl+"]"
                except Exception:
                    pass

def getDomainsFromBaidu(html):  
    soup = BeautifulSoup(html)
    html=soup.find('div', id="content_left")
    if html is None:
        print '[!] failed to crawl'
    else:
        html_doc=html.find_all('h3',class_="t")
        if html_doc is None:
            print '[!] failed to crawl'
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            for doc in html_doc:
                try:
                    href=doc.find('a')
                    link=href.get('href')
                    rurl=urllib2.urlopen(link.strip()).geturl()
                    url = rurl.strip()
                    reg='http:\/\/[^\/]+'
                    match_url = re.search(reg,url)
                    if match_url:
                        site=match_url.group(0)
                    if not isExisted(site,'subdomains.txt'):
                        logfile(site,'subdomains.txt')
                        print "[+] "+site
                    else:
                        print "[!] url is duplicate ["+site+"]"
                except Exception:
                    pass

def fetchUrls(se,wd,pg):
    if 'baidu' in se:
        for x in xrange(1,pg):
            rn=10
            pn=(x-1)*rn
            url='http://www.baidu.com/baidu?cl=3&tn=baidutop10&wd='+wd+'&rn='+str(rn)+'&pn='+str(pn)
            html=getUrlRespHtml(url)
            urls=getLinksFromBaidu(html)
    output = os.path.dirname(os.path.realpath(__file__))+"/urls.txt"
    if os.path.exists(output):
        print "\n[+] Fetched URLs:"
        print "[-] Output File: "+output

def scanSubDomains(se,wd,pg):
    if 'baidu' in se:
        wd="inurl:"+wd
        wd=wd.strip()
        for x in xrange(1,pg):
            rn=10
            pn=(x-1)*rn
            url='http://www.baidu.com/baidu?cl=3&tn=baidutop10&wd='+wd+'&rn='+str(rn)+'&pn='+str(pn)
            html=getUrlRespHtml(url)
            urls=getDomainsFromBaidu(html)
    output = os.path.dirname(os.path.realpath(__file__))+"/subdomains.txt"
    if os.path.exists(output):
        print "\n[+] Scanned SubDomains:"
        print "[-] Output File: "+output

def myhelp():
    print "\n+-----------------------------+"
    print "|  hackUtils v0.0.1           |"
    print "|  Avfisher - Wooyun.org      |"
    print "|  security_alert@126.com     |"
    print "+-----------------------------+\n"
    print "Usage: hackUtils.py [options]\n"
    print "Options:"
    print "  -h, --help                                  Show basic help message and exit"
    print "  -b keyword, --baidu=keyword                 Fetch URLs from Baidu.com based on specific keyword"
    print "  -d site, --domain=site                      Scan subdomains based on specific site"
    print "\nExamples:"
    print "  hackUtils.py -b inurl:www.example.com"
    print "  hackUtils.py -d example.com"
    print "\n[!] to see help message of options run with '-h'"

def main():
    try:
        options,args = getopt.getopt(sys.argv[1:],"hb:d:",["help","baidu=","domain="])
    except getopt.GetoptError:
        sys.exit()

    for name,value in options:
        if name in ("-h","--help"):
            myhelp()
        if name in ("-b","--baidu"):
            fetchUrls('baidu',value,10)
        if name in ("-d","--domain"):
            scanSubDomains('baidu',value,10)

if __name__ == '__main__':
    main()
