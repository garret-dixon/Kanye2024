from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, logout_user
import uuid
import models
import forms

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
login = LoginManager(app)

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/states', methods=['GET', 'POST'])
def index():
    state = db.session.query(models.State).all()
    return render_template('index.html', state = state)

@app.route('/state/<name>', methods = ['GET', 'POST'])
def state(name):
    state = db.session.query(models.State)\
        .filter(models.State.name == name).one()
    return render_template('state.html', state = state)

@app.route('/blog', methods = ['GET', 'POST'])
def blog():
    
    if current_user.is_authenticated:
        posts = reversed(db.session.query(models.BlogPost).all())
        form = forms.Blog()
        username = current_user.get_id()
        if form.validate_on_submit(): 
            if form.message.data is '':
                flash('Post cannot be blank')
                return redirect(url_for('blog'))      
            id = uuid.uuid1()
            db.session.execute('INSERT INTO BlogPost VALUES (:id, :username, :message)',
                               dict(id=id, username = username, message = form.message.data))
            db.session.commit()
            return redirect(url_for('blog'))
        return render_template('blog.html', posts = posts, form = form, username = username)
    return redirect(url_for('loginpage'))


@app.route('/login', methods = ['GET', 'POST'])
def loginpage():
    form = forms.Login()
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    if form.validate_on_submit():
        user = db.session.query(models.BlogUser).filter(models.BlogUser.id == form.username.data).first()
        if user is None or not user.password == form.password.data:
            flash('Invalid username or password')
            return redirect(url_for('loginpage'))
        login_user(user)
        return redirect(url_for('blog'))
    return render_template('login.html', form = form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = forms.Signup()
    

    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    if form.validate_on_submit():
        user = db.session.query(models.BlogUser).filter(models.BlogUser.id == form.username.data).first()
        if user is not None:
            flash('Username already taken')
            return redirect(url_for('signup'))
        if form.password.data is '':
            flash('Password cannot be blank')
            return redirect(url_for('signup'))
        if form.username.data is '':
            flash('Username cannot be blank')
            return redirect(url_for('signup'))
        db.session.execute('INSERT INTO Bloguser VALUES (:id, :password)',
                               dict(id=form.username.data, password = form.password.data))
        db.session.commit()
        return redirect(url_for('loginpage'))
    return render_template('signup.html', form = form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    logout_user()
    return redirect(url_for('home'))

@app.route('/usertest', methods = ['GET', 'POST'])
def usertest():
    users = db.session.query(models.BlogUser).all()
    return render_template('usertest.html', users = users)

@login.user_loader
def load_user(id):
    return db.session.query(models.BlogUser)\
        .filter(models.BlogUser.id == id).one()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)