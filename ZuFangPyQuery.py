import json
import time

from pyquery import PyQuery as pq

def startGetData(url):
    doc = pq(url=url)

    titles = doc('.content__list--item--aside')
    titleList = []
    hrefList = []
    for item in titles.items():
        titleList.append(item.attr('title'))
        hrefList.append('https://sh.zu.ke.com' + item.attr('href'))

    imgs = doc('.content__list--item--aside img')
    imgList = []
    for item in imgs.items():
        img = item.attr('data-src')
        imgList.append(img)

    locations = doc('.content__list--item--des')
    locationList = []
    for item in locations.items():
        locationList.append(item.text().strip())

    unitPrices = doc('.content__list--item-price')
    unitPriceList = []
    for item in unitPrices.items():
        unitPriceList.append(item.text().strip())

    timeInfos = doc('.content__list--item--time.oneline')
    timeInfoList = []
    for item in timeInfos.items():
        timeInfoList.append(item.text().strip())

    tags = doc('.content__list--item--bottom.oneline')
    tagList = []
    for item in tags.items():
        tagList.append(item.text().strip())

    i = 0
    for item in imgList:
        yield {
            'title': titleList[i],  # 标题
            'unitPrice': unitPriceList[i],  # 租金
            'location': locationList[i],  # 地址
            'time': timeInfoList[i],  # 发布时间
            'tag': tagList[i],  # 标签
            'href': hrefList[i],  # 跳转链接
            'image': imgList[i],  # 图片
        }
        i += 1

def write_to_file(content):
    with open('chengjiao.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + ',\n')

if __name__ == '__main__':
    url = 'https://sh.zu.ke.com/zufang/xuhui/pg'
    for i in range(5):
        param = url + str(i + 1) + '/'
        for item in startGetData(param):
            print(item)
            # write_to_file(item)
        time.sleep(1)