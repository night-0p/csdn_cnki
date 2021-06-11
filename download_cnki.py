import random
import re
import string
import urllib.request
import requests
from flask import Response
import getdb
import json
from bs4 import  BeautifulSoup
def get_cnki_content(url, cardpass):
    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163',
    }
    session = requests.session()
    r = session.get(url, headers=header)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')
    filename = soup.find(class_="title").string
    pdfurl = soup.find(id="pdfDown",).get("href")
    downurl = 'https://kns.cnki.net' + pdfurl
    my_proxies={"http":"socks5://182.92.218.110:123","https":"socks5://182.92.218.110:123"}
    resp=session.get(downurl,proxies=my_proxies,stream=True,timeout=1)
    def down():
        for chunk in resp.iter_content(chunk_size=512):
            if chunk:
                yield chunk

    response = Response(down(), content_type='application/octet-stream')  # 创建用个response对象
    # 文件名固定格式
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
        (filename + ".caj").encode().decode('latin-1'))
    return response
    db = getdb.getdb()  # 下载成功卡密被标记使用时间
    getid = db.query(cardpass)
    id = getid[0]
    db.updatetime(id)
    add(db)
    db.close()
    return response


def check(cardpass):  # 前台数据验证
    db = getdb.getdb()
    getid = db.query(cardpass)
    if getid == None:  # 没有这个卡密
        db.close()
        return False
    else:
        dtime = getid[1]
        if dtime != None:  # 卡密已经使用
            db.close()
            return False
        else:
            return True

def add(db=getdb.getdb()):  # 添加卡密
    cardpass = ''.join(random.sample(string.ascii_letters + string.digits, 18))  # 卡密为18位大小写加数字
    db.insert(cardpass)
    db.close()
def queryall():
    db=getdb.getdb()
    all=db.queryall()
    db.close()
    return all
def delete(list):
    try:
        db=getdb.getdb()
        db.delete(list)
        db.close()
        return True
    except Exception as e:
        return False