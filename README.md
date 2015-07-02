# hackUtils
It is a hack tool kit for pentest.

Usage: 

    hackUtils.py [options]

Options:

    -h, --help                                  Show basic help message and exit
    -b keyword, --baidu=keyword                 Fetch URLs from Baidu.com based on specific keyword
    -d site, --domain=site                      Scan subdomains based on specific site

Examples:

    hackUtils.py -b inurl:www.example.com
    hackUtils.py -d example.com

You need to install bs4 module http://www.crummy.com/software/BeautifulSoup/bs4/ by below command before you use this script:
        
    git clone https://github.com/kelp404/bs4 bs4
