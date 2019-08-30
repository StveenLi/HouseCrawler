import json
import time

from pyquery import PyQuery as pq

def startGetData(url):
    doc = pq(url=url)

    items1 = doc('.listUnit-date.clearfix.PBA_list_house')
    nameList = []
    catList = []
    variantList = []
    priceList = []
    for item in items1.items():
        nameList.append(item.attr('name'))
        catList.append(item.attr('category'))
        variantList.append(item.attr('variant'))
        priceList.append(int(item.attr('price')))

    items2 = doc('.pro-pic.li_phoneNum a')
    hrefList = []
    for item in items2.items():
        hrefList.append(item.attr('href'))

    items3 = doc('.pro-pic.li_phoneNum a .lazy')
    imgList = []
    for item in items3.items():
        imgList.append(item.attr('data-original'))

    items4 = doc('.list-pic-title h3 a')
    titleList = []
    for item in items4.items():
        titleList.append(item.attr('title'))

    items5 = doc('.list-pic-ps')
    infoList = []
    for item in items5.items():
        infoList.append(item.text())

    items6 = doc('.list-pic-ad')
    addrList = []
    for item in items6.items():
        addrList.append(item.text())

    items7 = doc('.pro-lable')
    tagList = []
    for item in items7.items():
        tagList.append(item.text())

    items8 = doc('.room-time')
    timeList = []
    for item in items8.items():
        timeList.append(item.text())

    i = 0
    for item in nameList:
        yield {
            'name': nameList[i],  #
            'category': catList[i],  #
            'variant': variantList[i],  #
            'price': priceList[i],  #
            'href': hrefList[i], #
            'img': imgList[i], #
            'title': titleList[i], #
            'house': infoList[i], #
            'address': addrList[i], #
            'remark': tagList[i], #
            'time': timeList[i] #
        }
        i += 1

def write_to_file(content):
    with open('baletu.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + ',\n')

if __name__ == '__main__':
    url = 'http://sh.baletu.com/zhaofang/p{pageNum}o1a1d900/?seachId=0&is_rec_house=0&entrance=14&solr_house_cnt=5176'

    i = 1
    while(i <= 10):
        param = url.format(pageNum=i)
        for item in startGetData(param):
            print(item)
            write_to_file(item)
        i += 1
        time.sleep(1)