# 应用文件
from flask import Flask, request, redirect, render_template, url_for, \
    session
import config
from models import User
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone, User.password == password).first()
        if not user:
            return '手机号码或密码错误，请确认后再登录！'
        session['user_id'] = user.id
        # 如果想31天内免登陆
        session.permanent = True
        return redirect(url_for('index'))
            

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        phone = request.form.get('phone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        ## 数据校验
        # 手机号码校验
        user = User.query.filter(User.phone == phone).first()
        if user:
            return '该手机号码已被注册，请更换手机号码！'
        # 密码校验
        if password1 != password2:
            return '两次输入的密码不相同，请核对后重新输入'
        # 校验成功，插入数据
        user = User(phone=phone,username=username,password=password1)
        db.session.add(user)
        db.session.commit()
        # 跳转到登录页面
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        pass


@app.context_processor
def my_context_procesor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)