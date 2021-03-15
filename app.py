from flask import Flask, render_template, request, session, Response
from sqlalchemy import desc

import config
from model import db, User, Article

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
db.create_all(app=app)


def isLogin():
    return 'uid' in session and session['uid']


@app.route('/')
def index():
    return render_template('list.html', alist=Article.query.order_by(desc(Article.create_time)))


@app.route('/a/<int:aid>')
def archive(aid):
    a: Article = Article.query.filter_by(id=aid).first()
    if not a:
        return Response('资源未找到', status=404)
    u = User.query.filter_by(id=a.uid).first()
    return render_template('archive.html', title=a.title, content=a.content, time=a.create_time, username=u.username)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method != 'POST':
        return render_template('register.html')

    username, password = request.form.get('username', ''), request.form.get('password', '')
    u = User()
    u.username = username
    u.password = password
    db.session.add(u)
    db.session.commit()
    return '注册成功'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')

    username, password = request.form.get('username', ''), request.form.get('password', '')
    a = User.query.filter_by(username=username, password=password).first()
    if a:
        session['uid'] = a.id
        return '登录成功'
    else:
        return '用户名或密码错误'


@app.route('/main')
def main():
    a = User.query.filter_by(id=session['uid']).first()
    return a.username


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method != 'POST':
        return render_template('publish.html')

    title, content = request.form.get('title', ''), request.form.get('content', '')
    a = Article()
    a.title = title
    a.content = content
    a.uid = session['uid']
    db.session.add(a)  # insert
    db.session.commit()
    return '发布成功'


@app.route('/edit/<int:aid>', methods=['GET', 'POST'])
def edit(aid):
    a: Article = Article.query.filter_by(id=aid).first()
    if not a:
        return Response('资源未找到', status=404)
    if request.method != 'POST':
        return render_template('edit.html', title=a.title, content=a.content)

    title, content = request.form.get('title', ''), request.form.get('content', '')
    a.title = title
    a.content = content
    a.uid = session['uid']
    db.session.merge(a)
    db.session.commit()
    return '发布成功'


if __name__ == '__main__':
    app.run()
