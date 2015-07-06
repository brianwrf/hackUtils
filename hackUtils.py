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
import hashlib
import base64

from bs4 import BeautifulSoup

# Ignore SSL error when accessing a HTTPS website
# ssl._create_default_https_context = ssl._create_unverified_context

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
    respHtml=''
    try:
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
    except Exception:
        pass
    return respHtml

def getLinksFromBaidu(html):  
    soup = BeautifulSoup(html)
    html=soup.find('div', id="content_left")
    if html is None:
        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
        print "["+str(now)+"] [WARNING] failed to crawl"
    else:
        html_doc=html.find_all('h3',class_="t")
        if html_doc is None:
            now = time.strftime('%H:%M:%S',time.localtime(time.time()))
            print "["+str(now)+"] [WARNING] failed to crawl"
        else:
            for doc in html_doc:
                try:
                    href=doc.find('a')
                    link=href.get('href')
                    rurl=urllib2.urlopen(link.strip()).geturl()
                    if not isExisted(rurl,'urls.txt'):
                        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
                        logfile(rurl,'urls.txt')
                        print "["+str(now)+"] [INFO] "+rurl
                    else:
                        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
                        print "["+str(now)+"] [WARNING] url is duplicate ["+rurl+"]"
                except Exception:
                    pass

def getDomainsFromBaidu(html,wd):  
    soup = BeautifulSoup(html)
    html=soup.find('div', id="content_left")
    if html is None:
        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
        print "["+str(now)+"] [WARNING] failed to crawl"
    else:
        html_doc=html.find_all('h3',class_="t")
        if html_doc is None:
            now = time.strftime('%H:%M:%S',time.localtime(time.time()))
            print "["+str(now)+"] [WARNING] failed to crawl"
        else:
            for doc in html_doc:
                try:
                    href=doc.find('a')
                    link=href.get('href')
                    rurl=urllib2.urlopen(link.strip()).geturl()
                    url = rurl.strip()
                    reg='http:\/\/[^\.]+'+'.'+wd
                    match_url = re.search(reg,url)
                    if match_url:
                        site=match_url.group(0)
                    if not isExisted(site,'subdomains.txt'):
                        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
                        logfile(site,'subdomains.txt')
                        print "["+str(now)+"] [INFO] "+site
                    else:
                        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
                        print "["+str(now)+"] [WARNING] url is duplicate ["+site+"]"
                except Exception:
                    pass

def getLinksFromWooyun(html):  
    soup = BeautifulSoup(html)
    soup = soup.find('div', class_="content")
    soup = soup.find('table',class_="listTable")
    html = soup.find('tbody')
    if html is None:
        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
        print "["+str(now)+"] [WARNING] failed to crawl"
    else:
        html_doc=html.find_all('tr')
        if html_doc is None:
            now = time.strftime('%H:%M:%S',time.localtime(time.time()))
            print "["+str(now)+"] [WARNING] failed to crawl"
        else:
            for doc in html_doc:
                try:
                    td=doc.find_all('td')[2]
                    atag=td.find('a')
                    link=atag.get('href').strip()
                    if not isExisted(link,'wooyun.txt'):
                        logfile(link,'wooyun.txt')
                        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
                        print "["+str(now)+"] [INFO] "+link
                    else:
                        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
                        print "["+str(now)+"] [WARNING] url is duplicate ["+link+"]"
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
    elif 'wooyun' in se:
        wooyun = os.path.dirname(os.path.realpath(__file__))+"/wooyun.txt"
        if not os.path.exists(wooyun):
            now = time.strftime('%H:%M:%S',time.localtime(time.time()))
            print "["+str(now)+"] [INFO] Fetching sites from Wooyun.org..."
            for i in xrange(1,38):
                url='http://www.wooyun.org/corps/page/'+str(i)
                html=getUrlRespHtml(url)
                getLinksFromWooyun(html)
            print "\n[INFO] Fetched Sites from Wooyun:"
            print "[*] Output File: "+wooyun
        links = open('wooyun.txt','r')
        for link in links:
            site = link.split("//")[1]
            if "www." in site:
                site=site.split("www.")[1]  
            kwd="inurl:"+site.strip()+"/"+wd.strip()
            print "\n[INFO] Scanned Site: "+site.strip()+"/"+wd.strip()
            for x in xrange(1,pg):
                rn=10
                pn=(x-1)*rn
                url='http://www.baidu.com/baidu?cl=3&tn=baidutop10&wd='+kwd+'&rn='+str(rn)+'&pn='+str(pn)
                html=getUrlRespHtml(url)
                urls=getLinksFromBaidu(html)
        links.close()
    output = os.path.dirname(os.path.realpath(__file__))+"/urls.txt"
    if os.path.exists(output):
        print "\n[INFO] Fetched URLs:"
        print "[*] Output File: "+output

def scanSubDomains(se,wd,pg):
    if 'baidu' in se:
        if "www." in wd:
            wd=wd.split("www.")[1]
        print "[INFO] Scanned Site: "+wd.strip()
        kwd="inurl:"+wd
        for x in xrange(1,pg):
            rn=10
            pn=(x-1)*rn
            url='http://www.baidu.com/baidu?cl=3&tn=baidutop10&wd='+kwd.strip()+'&rn='+str(rn)+'&pn='+str(pn)
            html=getUrlRespHtml(url)
            urls=getDomainsFromBaidu(html,wd.strip())
    output = os.path.dirname(os.path.realpath(__file__))+"/subdomains.txt"
    if os.path.exists(output):
        print "\n[INFO] Scanned SubDomains:"
        print "[*] Output File: "+output

def encryptStr(value):
    value=value.strip()
    md5=hashlib.md5(value).hexdigest()
    sha1=hashlib.sha1(value).hexdigest()
    sha256=hashlib.sha256(value).hexdigest()
    b64=base64.b64encode(value)
    print "[INFO] Clear Text: "+value
    print "[*] MD5: "+md5
    print "[*] SHA1: "+sha1
    print "[*] SHA256: "+sha256
    print "[*] Base64: "+b64
    
def myhelp():
    print "\n+-----------------------------+"
    print "|  hackUtils v0.0.1           |"
    print "|  Avfisher - Wooyun.org      |"
    print "|  security_alert@126.com     |"
    print "+-----------------------------+\n"
    print "Usage: hackUtils.py [options]\n"
    print "Options:"
    print "  -h, --help                                          Show basic help message and exit"
    print "  -b keyword, --baidu=keyword                         Fetch URLs from Baidu.com based on specific keyword"
    print "  -w keyword, --wooyun=keyword                        Fetch URLs from Wooyun Corps based on specific keyword"
    print "  -d site, --domain=site                              Scan subdomains based on specific site"
    print "  -e string, --encrypt=string                         Encrypt string based on specific encryption algorithms (e.g. base64, md5, sha1, sha256, etc.)"
    print "\nExamples:"
    print "  hackUtils.py -b inurl:www.example.com"
    print "  hackUtils.py -w .php?id="
    print "  hackUtils.py -d example.com"
    print "  hackUtils.py -e text"
    print "\n[!] to see help message of options run with '-h'"

def main():
    try:
        options,args = getopt.getopt(sys.argv[1:],"hb:w:d:e:",["help","baidu=","wooyun=","domain=","encrypt="])
    except getopt.GetoptError:
        print "\n[WARNING] error, to see help message of options run with '-h'"
        sys.exit()

    for name,value in options:
        if name in ("-h","--help"):
            myhelp()
        if name in ("-b","--baidu"):
            fetchUrls('baidu',value,50)
        if name in ("-w","--wooyun"):
            fetchUrls('wooyun',value,50)
        if name in ("-d","--domain"):
            scanSubDomains('baidu',value,50)
        if name in ("-e","--encrypt"):
            encryptStr(value)

if __name__ == '__main__':
    main()
