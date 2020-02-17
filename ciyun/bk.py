# -*- coding: utf-8 -*-
import requests
import re

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = "utf-8"
        print(r.text)
        return r.text
    except:
        return ''


def printAPPName(html):
    pass

def fillUnivlist(titles, comments, stars, html):
    try:
        pattern = re.compile(r'"title":{"label":(.*?)}, "content"', re.S) #提取标题
        nbaInfo = re.findall(pattern, str(html)) #提取title

        # findStr = '"title":{"label":'
        # nbaInfo = nbaInfo1[nbaInfo1.find(findStr)+len(findStr):]
        patternFloor = re.compile(r'"content":{"label":(.*?), "attributes":{"type":"text"}}', re.S) #提取content
        floorText = re.findall(patternFloor, str(html))

        patternStar = re.compile(r'"im:rating":{"label":(.*?)}, "id"', re.S)  # 提取星级
        star = re.findall(patternStar, str(html))
        # print(str(star))

        number = len(nbaInfo)
        print(number)
        for i in range(number):
            Info = nbaInfo[i] #利用Tools类移除不想要的格式字符
            if i==0:Info = Info[Info.find('"title":{"label":')+len('"title":{"label":'):]
            # print(Info)
            Info1 = floorText[i]
            Info2 = star[i]
            # print(Info2+"hello")
            titles.append('title:' + Info)
            comments.append(Info1)
            stars.append('star:' + Info2)
    except:
        return ''

def writeText(titleText, fpath):
    try:
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write(str(titleText)+'\n')
            f.write('\n')
            f.close()
    except:
        return ''

def writeUnivlist(titles, comments, stars, fpath, num):
    with open(fpath, 'a', encoding='utf-8') as f:
        for i in range(num):
            f.write(str(comments[i]) + '\n')
        f.close()

def main():
    count = 0
    url = 'https://itunes.apple.com/rss/customerreviews/page=1/id=1347663353/sortby=mostrecent/json?l=en&&cc=cn' #要访问的网址
    output_file = '贝壳.txt' #最终文本输出的文件
    html = getHTMLText(url) #获取HTML
    APPName = printAPPName(html)
    # print(html)
    writeText(APPName, output_file)
    for i in range(10):
        i = i + 1
        titles = []
        comments = []
        stars = []
        url = 'https://itunes.apple.com/rss/customerreviews/page=' + str(i) + '/id=1347663353/sortby=mostrecent/json?l=en&&cc=cn'
        html = getHTMLText(url)
        fillUnivlist(titles, comments, stars, html)
        writeUnivlist(titles, comments, stars, output_file, len(titles))
        # print(html)
        count = count + 1
        print("\r当前进度: {:.2f}%".format(count * 100 / 10), end="")
        
if __name__ == '__main__':
    main()