import json
import time

from pyquery import PyQuery as pq

def startGetData(url):
    doc = pq(url=url)

    titles = doc('.title a')
    titleList = []
    hrefList = []
    for item in titles.items():
        titleList.append(item.attr('title'))
        hrefList.append(item.attr('href'))

    i = 0
    for item in titleList:
        yield {
            'title': titleList[i],  # 标题
            'href': hrefList[i],  # 跳转链接 xUehVfSuh6>h
        }
        i += 1

def write_to_file(content):
    with open('douban.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + ',\n')

if __name__ == '__main__':
    url = 'https://www.douban.com/group/shanghaizufang/discussion?start='
    i = 0
    while(i <= 500):
        param = url + str(i)
        for item in startGetData(param):
            print(item)
            write_to_file(item)
        i += 25
        time.sleep(1)