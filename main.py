#!/usr/bin/env python3
import requests
import lxml.html as lh
import sys, os, subprocess

URL = 'https://spys.one'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/74.0.3729.169 Safari/537.36'
CONFIG_NAME = "proxychains4.conf"

def write_file(name, value):
    with open(name, 'wb') as f:
        f.write(value)

def main():
    #if os.geteuid() == 0:
    #    print("We're root!")
    #else:
    #    print("We're not root.")
    #    subprocess.call(['sudo', 'python3', *sys.argv])
    #    sys.exit()
    print("Trying to connect to spys.one")
    response = requests.get(URL, headers={"User-agent": USER_AGENT})
    assert response.status_code == 200
    print("200: OK")
    #write_file('main.html', response.content)
    doc = lh.fromstring(response.content)
    #print(doc.cssselect('body>table:nth-child(2)'))
    
    proxies = [(q[0].text_content().split(':'), 'http' if 'HTTP' in q[1].text_content() else q[1].text_content().lower()) \
        for i in doc.cssselect('body > \
        table:nth-child(2) > tr:nth-child(3) > td:nth-child(1) > table:nth-child(1) > \
        tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tr') if len(q:=i.cssselect('td'))>2][1:]
    print("Proxy list downloaded")

    #print(proxies)
    #try:
    with open(f'/etc/{CONFIG_NAME}', 'r') as f:
        lines = f.readlines()
        lines[lines.index('[ProxyList]\n')+1:] = [f"{proxy[1]} {proxy[0][0]} {proxy[0][1]}\n" for proxy in proxies]
    print("Proxychains config copied")
    #print(lines)
    with open(f'{CONFIG_NAME}', 'w+') as f:
        for line in lines:
            f.write(line)
    print("Config copy modified")
    #except:
    #    print('no permissions')


if __name__ == '__main__':
    main()