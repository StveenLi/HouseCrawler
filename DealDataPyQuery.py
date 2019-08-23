# 利用pyquery抓取二手房成交数据

import json
import time

from pyquery import PyQuery as pq

def startGetData(url):
    doc = pq(url=url)

    imgs = doc('.img.CLICKDATA.maidian-detail img')
    imgList = []
    for item in imgs.items():
        imgList.append(item.attr('data-original'))

    titles = doc('.listContent li .info .title a')
    titleList = []
    hrefList = []
    for item in titles.items():
        titleList.append(item.text().strip())
        hrefList.append(item.attr('href'))

    dealDates = doc('.info .dealDate')
    dealDateList = []
    for item in dealDates.items():
        dealDateList.append(item.text().strip())

    houseInfos = doc('.info .houseInfo')
    houseInfoList = []
    for item in houseInfos.items():
        houseInfoList.append(item.text().strip())

    totalPrices = doc('.info .totalPrice .number')
    totalPriceList = []
    for item in totalPrices.items():
        totalPriceList.append(item.text().strip() + '万')

    unitPrices = doc('.info .flood .unitPrice')
    unitPriceList = []
    for item in unitPrices.items():
        unitPriceList.append(item.text().strip())

    positionInfos = doc('.info .flood .positionInfo')
    positionInfoList = []
    for item in positionInfos.items():
        positionInfoList.append(item.text().strip())

    dealCycleeInfos = doc('.info .dealCycleeInfo .dealCycleTxt')
    dealCycleeInfoList = []
    for item in dealCycleeInfos.items():
        dealCycleeInfoList.append(item.text().strip())

    i = 0
    for item in imgList:
        yield {
            'title': titleList[i],  # 标题
            'totalPrice': totalPriceList[i],  # 总价
            'unitPrice': unitPriceList[i],  # 单价
            'dealDate': dealDateList[i],  # 房源成交时间
            'dealInfo': dealCycleeInfoList[i],  # 挂牌信息
            'href': hrefList[i],  # 跳转链接
            'image': imgList[i],  # 图片
            'houseInfo': houseInfoList[i] + positionInfoList[i],  # 房源描述
        }
        i += 1

def write_to_file(content):
    with open('deal.txt', 'a', encoding='utf-8') as f:f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    url = 'https://hf.ke.com/chengjiao/feixi/pg'
    for i in range(10):
        param = url + str(i + 1) + '/'
        for item in startGetData(param):
            print(item)
            write_to_file(item)
        time.sleep(1)