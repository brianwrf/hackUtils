# hackUtils
It is a hack tool kit for pentest and web security research, which is based on BeautifulSoup module http://www.crummy.com/software/BeautifulSoup/bs4/. 

Please firstly install bs4 module before using this script by below command:

    git clone https://github.com/kelp404/bs4 bs4

Usage: 

    hackUtils.py [options]

Options:

    -h, --help                                  Show basic help message and exit
    -b keyword, --baidu=keyword                 Fetch URLs from Baidu.com based on specific keyword
    -d site, --domain=site                      Scan subdomains based on specific site
    -e string, --encrypt=string                 Encrypt string based on specific encryption algorithms (e.g. base64, md5, sha1, sha256, etc.)


Examples:

    hackUtils.py -b inurl:www.example.com
    hackUtils.py -d example.com
    hackUtils.py -e text
