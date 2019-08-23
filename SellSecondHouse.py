#抓取合肥在售二手房

import time
import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_two_page(html):
    soup = BeautifulSoup(html, 'lxml')

    items = soup.find_all(attrs={'class': 'img VIEWDATA CLICKDATA maidian-detail'})
    items1 = soup.find_all(attrs={'class': 'positionInfo'})
    items2 = soup.find_all(attrs={'class': 'houseInfo'})
    items3 = soup.find_all(attrs={'class': 'followInfo'})
    items4 = soup.find_all(attrs={'class': 'totalPrice'})
    items5 = soup.find_all(attrs={'class': 'unitPrice'})

    i = 0
    for item in items:
        yield {
            'flood': parse_flood(items1, i),  # 小区
            'title': item.attrs['title'],  # 标题
            'href': item.attrs['href'],  # 跳转链接
            'alt': item.img['alt'],  # 描述
            'totalPrice': items4[i].span.text,  # 总价
            'unitPrice': items5[i].span.text,  # 单价
            'houseInfo': items2[i].text.strip(),  # 房源描述
            'followInfo': items3[i].text.strip()  # 房源发布时间及关注度
        }
        i += 1


def parse_flood(items1, i):
    if(items1[i].a != None):
        return items1[i].a.text
    else:
        return ''

def write_to_file(content):
    with open('sell.txt', 'a', encoding='utf-8') as f:f.write(json.dumps(content, ensure_ascii=False) + '\n')

def startGetData(page, *district):
    url = 'https://hf.ke.com/ershoufang/'

    addrParam = ''
    for param in district:
        addrParam = str(param)
    if (len(addrParam) > 0):
        url = url + addrParam + '/pg'
    else:
        url = url + 'pg'

    for i in range(page):
        param = url + str(i + 1) + '/'
        html = get_one_page(param)
        for item in parse_two_page(html):
            print(item)
            write_to_file(item)
        time.sleep(1)

if __name__ == '__main__':
    startGetData(10, 'feixi')