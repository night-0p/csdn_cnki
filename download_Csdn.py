import random
import re
import string
import urllib.request
import requests
from flask import Response
import getdb
import json
from bs4 import  BeautifulSoup
import time
def get_id(user_url):
    return user_url.split('/')[5]

def get_filename(response_source_url):
    filename_code=re.search(r'filename%3D%22(.+?)%22&', response_source_url)[1]
    filename=urllib.parse.unquote((urllib.parse.unquote(filename_code)))
    return filename
#url='https://download.csdn.net/source/download?source_id=12177668'
header_csdn = {
    'Cookie':'uuid_tt_dd=10_6108401710-1570018068062-403686; dc_session_id=10_1570018068062.515548; __gads=ID=98ddee1f77286313:T=1577421045:S=ALNI_Mb-yB6tCJQw4jlnT58GPkaJ9TTDCA; UN=lengfenghacker; _ga=GA1.2.1400328094.1582445592; UserName=lengfenghacker; UserInfo=a5154c9087c3441ea881e7f373e93140; UserToken=a5154c9087c3441ea881e7f373e93140; UserNick=HawkEyeTeam; AU=DA9; BT=1582463421996; p_uid=U100000; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=5744*1*lengfenghacker!6525*1*10_6108401710-1570018068062-403686!1789*1*WAP_VC; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1582518405; Hm_ct_e5ef47b9f471504959267fd614d579cd=5744*1*lengfenghacker!6525*1*10_6108401710-1570018068062-403686; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1585340316,1585382141,1585386054,1585389421; c_ref=https%3A//www.google.com/; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblog.csdn.net%252Fblogdevteam%252Farticle%252Fdetails%252F105203745%2522%252C%2522announcementCount%2522%253A1%252C%2522announcementExpire%2522%253A244074514%257D; TY_SESSION_ID=72881e57-f646-4c79-9e07-b8f63098bbbe; firstDie=1; dc_tos=q80ior;',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Accept-Encoding':'gzip, deflate, br',
    #'X-Requested-With':'XMLHttpRequest',
    #'X-Tingyun-Id':'im-pGljNfnc;r=609094656',
    #'sec-fetch-user':'?1',
    'referer':'https://download.csdn.net/my/downloads',
    #'sec-fetch-mode':'navigate',
    #'sec-fetch-site':'same-origin',
    #'upgrade-insecure-requests':'1'
}
header_csdn2={
    'referer':'https://download.csdn.net/my/downloads',
}


def get_csdn_content(user_url,cardpass):
   
    source_url='https://download.csdn.net/source/download?source_id='+get_id(user_url)
    session=requests.session()
    get_download_url = session.get(source_url,headers=header_csdn)


    download_url=json.loads(get_download_url.text)['data']
    
    text = session.get(download_url, headers=header_csdn2,stream=True)
    
     
    def down():
        for chunk in text.iter_content(chunk_size=512):
            if chunk:
                yield chunk
    response=Response(down(),content_type='application/octet-stream')
    response.headers['Content-Disposition']='attachment; filename={}'.format((get_filename(download_url)).encode().decode('latin-1'))
    response.headers['Content-Length']=text.headers['Content-Length']
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
       