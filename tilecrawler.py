# -*- coding: UTF-8 -*-

#爬取地图瓦片数据
from urllib import request
import re
import urllib.request
import os
import random
import math
import sys

agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1']

# 经纬度反算切片行列号 3857坐标系
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)
 
 
# 下载图片
def getimg(Tpath, Spath, x, y):
    try:
        f = open(Spath, 'wb')
        req = urllib.request.Request(Tpath)
        req.add_header('User-Agent', random.choice(agents))  # 换用随机的请求头
        pic = urllib.request.urlopen(req, timeout=60)
 
        f.write(pic.read())
        f.close()
        print(str(x) + '_' + str(y) + '下载成功')
    except Exception:
        print(str(x) + '_' + str(y) + '下载失败,重试' + Tpath)
        getimg(Tpath, Spath, x, y)
 
def main():
    zoom=0
    left=0
    top=0
    right=0
    bottom=0
    outputpath=''
    if len(sys.argv) >= 7:
        zoom=int(sys.argv[1])
        left=float(sys.argv[2])
        top=float(sys.argv[3])
        right=float(sys.argv[4])
        bottom=float(sys.argv[5])
        outputpath=sys.argv[6]
    else:
        print("python tilecrawler.py zoom left top right bottom outputpath")
        exit()
    
    print(zoom)
    print(left)
    print(top)
    print(right)
    print(bottom)
    print(outputpath)
    lefttop = deg2num(top, left, zoom)  # 下载切片的左上角角点
    rightbottom = deg2num(bottom, right, zoom)

    print(lefttop)
    print(rightbottom)

    print("共" + str(lefttop[0] - rightbottom[0]))
    print("共" + str(lefttop[1] - rightbottom[1]))


    for x in range(lefttop[0], rightbottom[0]):
        for y in range(lefttop[1], rightbottom[1]):
            #Google地图瓦片
            #tilepath = 'http://www.google.cn/maps/vt/pb=!1m4!1m3!1i'+str(zoom)+'!2i'+str(x)+'!3i'+str(y)+'!2m3!1e0!2sm!3i345013117!3m8!2szh-CN!3scn!5e1105!12m4!1e68!2m2!1sset!2sRoadmap!4e0'
            #Google影像瓦片
            #tilepath = 'http://mt2.google.cn/vt/lyrs=y&hl=zh-CN&gl=CN&src=app&x='+str(x)+'&y='+str(y)+'&z='+str(zoom)+'&s=G'
            #天地图-地图
            #tilepath = 'http://t4.tianditu.com/DataServer?T=vec_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=45c78b2bc2ecfa2b35a3e4e454ada5ce'
            #天地图-标注
            #tilepath = 'http://t3.tianditu.com/DataServer?T=cva_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=45c78b2bc2ecfa2b35a3e4e454ada5ce'
            #天地图-影像
            #tilepath = 'http://t2.tianditu.gov.cn/DataServer?T=img_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=2ce94f67e58faa24beb7cb8a09780552'
            #天地图-影像标注
            #tilepath = 'http://t2.tianditu.gov.cn/DataServer?T=cia_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=2ce94f67e58faa24beb7cb8a09780552'
            # 腾讯地图影像瓦片
            y=int(2.0 ** zoom-y)
            tilepath = 'http://p0.map.gtimg.com/sateTiles/'+str(zoom)+'/'+str(int(x/16))+'/'+str(int(y/16))+'/'+str(x)+'_'+str(y)+'.jpg'
            path = outputpath + '/' + str(zoom) + '/' + str(x)
            if not os.path.exists(path):
                os.makedirs(path)
            getimg(tilepath, os.path.join(path, str(y) + ".png"), x, y)
    print('finish')

if __name__ == '__main__':
    main()

 
