import random
import string
import getdb





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
            
def sign_cardpass(cardpass):
    db = getdb.getdb()  # 下载成功卡密被标记使用时间
    getid = db.query(cardpass)
    id = getid[0]
    db.updatetime(id)
    add(db)
    db.close()

def updatatime_testnow():
    db=getdb.getdb()
    db.updatatime_testnow()
    db.close()

def Scardpass_dtime_isnull(cardpass):
    db=getdb.getdb()
    db.Scardpass_dtime_isnull(cardpass)
    db.close()

def add(db=getdb.getdb()):  # 添加卡密
    cardpass = ''.join(random.sample(string.ascii_letters + string.digits, 18))  # 卡密为18位大小写加数字
    db.insert(cardpass)
    db.close()

def queryall():
    db=getdb.getdb()
    all=db.queryall()
    db.close()
    return all

def queryall_testnow():
    db=getdb.getdb()
    all=db.queryall_testnow()
    db.close()
    return all

def get_testnow():
    db=getdb.getdb()
    info=db.get_testnow()
    db.close()
    return info

def upload_testnow(file):
    db=getdb.getdb()
    f=file
    user_list=[]
    password_list=[]
    phone_list=[]
    for i in f.readlines():
        line=i.decode("gbk")
        user=line.split(',')[0]
        user_list.append(user)
        password=line.split(',')[1]
        password_list.append(password)
        phone=line.split(',')[2].replace('\n','')
        phone_list.append(phone)
    
    db.upload_testnow(user_list,password_list,phone_list)   
def delete(list):
    try:
        db=getdb.getdb()
        db.delete(list)
        db.close()
        return True
    except Exception as e:
        return False
def detele_testnow(list):
    try:
        db=getdb.getdb()
        db.delete_testnow(list)
        db.close()
        return True
    except Exception as e:
        return False