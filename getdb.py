import pymysql
class getdb:
    host = ''
    user = ''
    password = ''
    database = ''
    db=''
    def __init__(self,host='localhost',user='root',password='esz87723',databse='test'):
        self.database=databse
        self.password=password
        self.user=user
        self.host=host
        try:
            mydb=pymysql.connect(
                host=self.host,
                port=3306,
                user=self.user,
                password=self.password,
                db=self.database,
                charset='utf8'
            )
        except Exception as e:
            print("数据库连接失败"+e)
            exit()
        self.db=mydb
    def insert(self,key):
        sql="INSERT into test(cardpass,ctime) values(%s,now())"
        value=(key,)
        self.db.cursor().execute(sql, value)
        self.db.commit()
    def delete(self,ids):
        sql="DELETE  from test where id=%s"
        values=[]
        for id in ids:
            value = (id,)
            values.append(value)
        self.db.cursor().executemany(sql,values)
        self.db.commit()
    def updatetime(self,id):
        id=int(id)
        sql="update test set dtime=now() where id=%s"
        value=(id,)
        self.db.cursor().execute(sql, value)
        self.db.commit()
    def queryall(self):
        mycursor = self.db.cursor()
        mycursor.execute("SELECT id,cardpass,ctime,dtime FROM test")
        myresult = mycursor.fetchall()
        return myresult
    def query(self,cardpass):
        mycursor = self.db.cursor()
        value = (cardpass,)
        mycursor.execute("SELECT id,dtime FROM test where cardpass=%s",value)
        myresult = mycursor.fetchone()
        return myresult
    def queryall_testnow(self):
        mycursor = self.db.cursor()
        mycursor.execute("SELECT id,user,password,phone,dtime FROM testnow")
        myresult = mycursor.fetchall()
        return myresult    

    def get_testnow(self):
        mycursor = self.db.cursor()
        mycursor.execute("SELECT id,user,password,phone FROM testnow where dtime is null")
        myresult = mycursor.fetchone()
        return myresult

    def updatatime_testnow(self):
        id=int(self.get_testnow()[0])
        sql="update testnow set dtime=now() where id=%s"
        value=(id,)
        self.db.cursor().execute(sql, value)
        self.db.commit()

    def Scardpass_dtime_isnull(self,cardpass):
        sql="update testnow set dtime=null where cardpass=%s"
        value=(cardpass,)
        self.db.cursor().execute(sql, value)
        self.db.commit()

    def upload_testnow(self,user_list,password_list,phone_list):
        sql="INSERT into testnow(user,password,phone) values(%s,%s,%s)"
        values=list(zip(user_list,password_list,phone_list))
        self.db.cursor().executemany(sql,values)
        self.db.commit()        
    def delete_testnow(self,ids):
        sql="DELETE  from testnow where id=%s"
        values=[]
        for id in ids:
            value = (id,)
            values.append(value)
        self.db.cursor().executemany(sql,values)
        self.db.commit()
    def close(self):
        self.db.close
