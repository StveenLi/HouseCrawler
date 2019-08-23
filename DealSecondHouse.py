# 利用BeautifulSoup抓取二手房成交数据

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

    items = soup.find_all(attrs={'class': 'img CLICKDATA maidian-detail'})
    items1 = soup.find_all(attrs={'class': 'CLICKDATA maidian-detail'})
    items2 = soup.find_all(attrs={'class': 'houseInfo'})
    items3 = soup.find_all(attrs={'class': 'positionInfo'})
    items4 = soup.find_all(attrs={'class': 'totalPrice'})
    items5 = soup.find_all(attrs={'class': 'unitPrice'})
    items6 = soup.find_all(attrs={'class': 'dealCycleTxt'})
    items7 = soup.find_all(attrs={'class': 'dealDate'})

    i = 0
    for item in items:
        yield {
            'title': items1[i].text.strip(),  # 标题
            'totalPrice': items4[i].span.text + '万',  # 总价
            'unitPrice': items5[i].span.text + '元/平米',  # 单价
            'dealDate': items7[i].text.strip(),  # 房源成交时间
            'dealPrice': items6[i].span.text,  # 挂牌价
            'dealTime': parse_chengjiao(items6, i), # 成交周期
            'href': item.attrs['href'],  # 跳转链接
            'image': item.img['data-original'],  # 图片
            'houseInfo': items2[i].text.strip() + items3[i].text.strip(),  # 房源描述
        }
        i += 1


def parse_chengjiao(items6, i):
    guaTime = ''
    for item in items6[i]:
        strDf = str(item)
        if (strDf.find('成交周期', 0, len(strDf)) > -1):
            guaTime = strDf[6:len(strDf) - 7]
    return guaTime

def write_to_file(content):
    with open('deal.txt', 'a', encoding='utf-8') as f:f.write(json.dumps(content, ensure_ascii=False) + '\n')

def startGetData(page, *district):
    url = 'https://hf.ke.com/chengjiao/'

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
    # 抓取数据 参数一：总页数，参数二：区县，可选、不传默认全部
    startGetData(10, 'feixi')