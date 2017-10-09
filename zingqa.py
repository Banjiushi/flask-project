# 应用文件
from flask import Flask, request, redirect, render_template, url_for, \
    session, g
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone).first()
        if not (user and user.check_password(password)):
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
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/d/<question_id>')
@login_required
def detail(question_id):
    question = Question.query.filter(Question.id==question_id).first()
    quest = Question.query.get(question_id)
    num = len(quest.answer)
    return render_template('detail.html', question=question, num=num)


@app.route('/add_answer', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    answer.author = g.user
    question =Question.query.filter(Question.id==question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/search')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html', questions=questions)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_procesor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)