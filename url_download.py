import re
import os
from bs4 import BeautifulSoup
user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.5) Gecko/20091123 Iceweasel/3.5.5 (like Firefox/3.5.5; Debian-3.5.5-1)"

def is_citeseer(url):
    return len(re.findall("citeseer", url)) > 0

def is_researchgate(url):
    return len(re.findall("researchgate", url)) > 0

def is_science_direct(url):
    return len(re.findall("sciencedirect", url)) > 0

def is_dtic(url):
    return len(re.findall("dtic\.mil", url)) > 0

def is_semanticscholar(url):
    return len(re.findall("semanticscholar", url)) > 0

def mod_citeseer(url):
    file_type = url[-3:]
    url = url.replace("summary", "download")
    url += "x"
    url = re.findall("^[^0-9]+doi=[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[^0-9]", url)[0][:-1] + "&rep=rep1&type=pdf"
    return url, file_type


def down_researchgate(url):
    os.system("curl -O -L --connect-timeout 20 --max-time 60 \"%s\"" % (url))

def down_citeseer(url):
    url, file_type = mod_citeseer(url)
    os.system("curl -L -o download.%s --connect-timeout 20 --max-time 60 \"%s\"" % (file_type, url))

def down_dtic(url):
    os.system("curl \"%s\" -H \"Connection: keep-alive\" -H \"Upgrade-Insecure-Requests: 1\" -H \"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36\" -H \"Sec-Fetch-Mode: navigate\" -H \"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\" -H \"Sec-Fetch-Site: none\" -H \"Accept-Encoding: gzip, deflate, br\" -H \"Accept-Language: zh-CN,zh;q=0.9,en;q=0.8\" --compressed -O" % (url))

def down_science_direct(url):
    print("Science Direct Detected!")

def down_semanticscholar(url):
    os.system("curl -L -o tmp.tmp \"%s\"" % (url))
    try:
        html = open("tmp.tmp", encoding = "utf-8").read()
        if len(re.findall("html", html)) > 0:
            soup = BeautifulSoup(html, "lxml")
            if len(soup.select('a[class="icon-button button--full-width button--primary"]')) > 0:
                new_url = soup.select('a[class="icon-button button--full-width button--primary"]')[0]#.findall("a", href = True)
                new_url = str(new_url.get("href"))
                os.system("curl -L -O \"%s\"" % (new_url))
                try:
                    os.remove("tmp.tmp")
                except:
                    pass
    except:
        os.remove("tmp.tmp")
        os.system("curl -L -O \"%s\"" % (url))
    

def download(url = "http://www.baidu.com", dir = "./"):
    os.system("set https_proxy=127.0.0.1:1080")
    os.system("set http_proxy=127.0.0.1:1080")
    pwd = os.getcwd()
    os.chdir(dir)

    if is_citeseer(url):
        down_citeseer(url)
    
    elif is_researchgate(url):
        down_researchgate(url)

    elif is_science_direct(url):
        down_science_direct(url)

    elif is_dtic(url):
        down_dtic(url)
    
    elif is_semanticscholar(url):
        down_semanticscholar(url)

    else:
        os.system("curl -L -O \"%s\"" % (url))
    os.chdir(pwd)
