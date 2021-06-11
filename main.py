from flask import Flask, render_template, request, session, redirect, url_for,abort,make_response
from flask_cors import *
from download_Csdn import get_csdn_content,get_filename
from download_cnki import get_cnki_content
import controller

pwd1 = 'ldtbvip.comcclengfeng'  # 密码
login1='/ldtbvipmyl0gin'
show1='/show1/'
show_admin="/show1/admin"
show_CSDN="/show1/test2"
showpage_csdn='/csdn'
showpage_cnki='/cnki' 
add1='/add1'
delete1='/delete1'
showpage_Testnow='/Testnow'
delete_testnow='/show1/delete1'
upload_testnow='/show1/upload'


app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['SECRET_KEY'] = pwd1
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

@app.errorhandler(InvalidUsage)
def invalid_usage(error):
    print(error.status_code)
    response = make_response(error.message)
    response.status_code = error.status_code
    return response

@app.route(login1, methods=['GET', 'POST'])  # 登录模块login=/login
def login():
    if request.method == 'GET':
        return render_template('login.html',login=login1)
    if request.method == 'POST':
        password = request.form['password']
        if password == pwd1:
            session['login'] = True
            return redirect(url_for('show_page'))
        else:
            session['login'] = False
            return "<script>alert('密码错误');window.history.back();</script>"


@app.route(add1)
def add():
    if session.get('login'):
        try:
            controller.add()
            return "<script>self.location=document.referrer;</script>"
        except Exception as e:
            return "<script>alert('添加失败');window.history.back();</script>"
    else:
        return "<script>alert('请先登录');window.location.href='"+login1+"'</script>"


@app.route(delete1, methods=["POST"])
def delete() -> str:
    if session.get('login'):
        list = request.form.getlist('item')
        if len(list) == 0:
            return "<script>alert('未选中任何选项');window.history.back();</script>"
        if controller.delete(list):  # 删除成功
            return "<script>alert('删除成功');self.location=document.referrer;</script>"
        else:
            return "<script>alert('删除失败');window.history.back();</script>"
    else:
        return "<script>alert('请先登录');window.location.href='"+str(login1)+"'</script>"

@app.route(delete_testnow, methods=["POST"])
def deletes_testnow() -> str:
    if session.get('login'):
        list = request.form.getlist('item')
        if len(list) == 0:
            return "<script>alert('未选中任何选项');window.history.back();</script>"
        if controller.detele_testnow(list):  # 删除成功
            return "<script>alert('删除成功');self.location=document.referrer;</script>"
        else:
            return "<script>alert('删除失败');window.history.back();</script>"
    else:
        return "<script>alert('请先登录');window.location.href='"+str(login1)+"'</script>"


@app.route(show1)
def show_page():  # 后台首页
    if session.get('login'):
        allinfo = controller.queryall_testnow()
        return render_template('admin.html', result=allinfo,add=add1,delete=delete_testnow)
    else:
        return "<script>alert('请先登录');window.location.href='"+login1+"'</script>"

@app.route(showpage_csdn)
def show_page_icsdn():  
        return render_template('Csdn.html')

@app.route(showpage_Testnow)
def show_page_iTestnow():  
        return render_template('Testnow.html')

@app.route(showpage_cnki)
def show_page_icnki(): 
        return render_template('Cink.html')

@app.route(show_admin)
def show_page2():  
    if session.get('login'):
        allinfo = controller.queryall_testnow()
        return render_template('admin.html', result=allinfo,delete=delete_testnow)
    else:
        return "<script>alert('请先登录');window.location.href='"+login1+"'</script>"

@app.route(upload_testnow,methods = ['GET', 'POST'])
def uploads_testnow():  
    if session.get('login'):
        file = request.files['file']
        controller.upload_testnow(file)
        return "<script>alert('上传成功');self.location=document.referrer;</script>"
    else:
        return "<script>alert('请先登录');window.location.href='"+login1+"'</script>"

@app.route(show_CSDN)
def show_page3():  
    if session.get('login'):
        allinfo=controller.queryall()
        return render_template('c_test2.html',result=allinfo,add=add1,delete=delete1)
    else:
        return "<script>alert('请先登录');window.location.href='"+login1+"'</script>"




@app.route('/downloadcsdn', methods=["POST"])
def downloadcsdn() -> str:  # 下载页面
    print("hallowrold")
    data = request.get_json(silent=True)
    url = data['url']
    print(url)
    cardpass = data['number']
    print(cardpass)
    if controller.check(cardpass):
        return get_csdn_content(url, cardpass)
    else:
        raise InvalidUsage('',400)


@app.route('/downloadcnki', methods=["POST"])
def downloadcnki() -> str:  # 下载页面

    print("hallowrold")
    data = request.get_json(silent=True)
    url = data['url']
    print(url)
    cardpass = data['number']
    print(cardpass)
    if url == '' or cardpass == '':
        return "<script>alert('参数不能为空');window.history.go(-1);</script>"
    else:
        if controller.check(cardpass):
            return get_cnki_content(url,cardpass)
        else:
            return "<script>alert('卡密错误');window.history.go(-1);</script>"

@app.route('/downloadtestnow', methods=["POST"])
def downloadtestnow() -> str:  # 下载页面
    cardpass = request.form['number']
    allinfo=controller.get_testnow()
    if cardpass == '':
        return "<script>alert('参数不能为空');window.history.go(-1);</script>"
    else:
        if controller.check(cardpass):
            controller.sign_cardpass(cardpass)
            controller.updatatime_testnow()
            return render_template('Testnow.html', result=allinfo)
        else:
            return "<script>alert('卡密错误');window.history.go(-1);</script>"


@app.route('/')
def entry_page():  # 首页
    return render_template('Testnow.html')
app.run(host='0.0.0.0', port=5013)
