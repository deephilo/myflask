from flask import Flask
from flask import redirect, url_for
from flask import request, render_template
from flask import make_response
from flask import Flask, session, escape
app = Flask(__name__)

#在url最后添加/，访问/blog/<int:postID>/或/blog/<int:postID>均可
@app.route('/blog/<int:postID>/')
def show_blog(postID):
   return 'Blog Number %d' % postID

#在url最后未添加，不可访问/rev/<float:postID>/,否则会报错：404 NOT FOUND
@app.route('/rev/<float:revNo>')
def revision(revNo):
   return 'Revision Number %f' % revNo


#url_for()函数对于动态构建特定函数的URL,第一个参数是指定函数，第二个参数是指定传递的参数名
@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest', guest = name))

#POST GET方法
@app.route('/login_in')
def login_in():
    return render_template("login.html")

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      print(1)
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      print(2)
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

#向模板传值
@app.route('/sendvalue')
def sendvalue():
    my_int = 18
    my_str = 'curry'
    my_list = [1, 5, 4, 3, 2]
    my_dict = {
        'name': 'durant',
        'age': 28
    }

    # render_template方法:渲染模板
    # 参数1: 模板名称  参数n: 传到模板里的数据
    return render_template('send_value.html',
                           my_int=my_int,
                           my_str=my_str,
                           my_list=my_list,
                           my_dict=my_dict)

#在模板中使用js
@app.route("/say_hello")
def sayhello():
   return render_template("say_hello.html")

@app.route('/student')
def student():
   return render_template('student.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)
   else:
      result = request.args.get
      return render_template("result.html",result = result)

#cookies
@app.route("/set_cookies")
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("w3cshool", "w3cshool",max_age=3600)
    return resp

@app.route("/get_cookies")
def get_cookie():
    cookie_1 = request.cookies.get("w3cshool")  # 获取名字为Itcast_1对应cookie的值
    return cookie_1

@app.route("/delete_cookies")
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie("w3cshool")
    return resp

#会话
app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return '登录用户名是:' + username + '<br>' + \
               "<b><a href = '/logout'>点击这里注销</a></b>"
    return "您暂未登录， <br><a href = '/login2'></b>" + \
           "点击这里登录</b></a>"

@app.route('/login2', methods = ['GET', 'POST'])
def login2():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
           <form action = "" method = "post">
               <p><input type="text" name="username"/></p>
               <p><input type="submit" value ="登录"/></p>
           </form>
           '''

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))


#重定向和错误


if __name__ == '__main__':
   app.run(debug = True)
