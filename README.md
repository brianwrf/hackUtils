# hackUtils
It is a hack tool kit for pentest and web security research, which is based on BeautifulSoup bs4 module http://www.crummy.com/software/BeautifulSoup/bs4/. 

Usage: 

    hackUtils.py [options]

Options:

    -h, --help                                  Show basic help message and exit
    -b keyword, --baidu=keyword                 Fetch URLs from Baidu based on specific keyword
    -g keyword, --google=keyword                Fetch URLs from Google based on specific keyword
    -w keyword, --wooyun=keyword                Fetch URLs from Wooyun Corps based on specific keyword
    -j url|file, --joomla=url|file              Exploit SQLi for Joomla 3.2 - 3.4
    -d site, --domain=site                      Scan subdomains based on specific site
    -e string, --encrypt=string                 Encrypt string based on specific encryption algorithms (e.g. base64, md5, sha1, sha256, etc.)


Examples:

    hackUtils.py -b inurl:www.example.com
    hackUtils.py -g inurl:www.example.com
    hackUtils.py -w .php?id=
    hackUtils.py -j http://www.joomla.com/
    hackUtils.py -j urls.txt
    hackUtils.py -d example.com
    hackUtils.py -e text
