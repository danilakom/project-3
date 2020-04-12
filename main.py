from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask import Flask, render_template, redirect, abort, request
from werkzeug.utils import secure_filename
from data import db_session
from data.users import User
from data.realties import Realties
from login import LoginForm
from add_realty import Add_Realty
from register import RegisterForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
PHOTOS_PATH = '/static/img'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/')
def index():
    realties = session.query(Realties)
    realtor = {}
    for realty in realties:
        user = session.query(User).filter(User.id == realty.realtor).first()
        if user:
            realtor[realty.id] = ' '.join([user.name, user.surname])
        else:
            realtor[realty.id] = ''
    return render_template('index.html', realties=realties, realtor=realtor, title='Недвижимость')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               title="Авторизация",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_realty', methods=['GET', 'POST'])
@login_required
def add_realty():
    form = Add_Realty()
    if form.validate_on_submit():
        session = db_session.create_session()
        realty = Realties()
        n, f = form.realtor.data.split(' ')
        yes = False
        for user in session.query(User).all():
            if user.name == n and user.surname == f:
                yes = True
                realty.realtor = user.id
                break
        if not yes:
            return render_template('add_realty.html',
                               message="Такого риэлтора не сущестсвует",
                               title="Добавление недвижимости",
                               form=form)
        realty.house = form.house.data
        realty.not_solded_flats = form.not_solded_flats.data
        realty.address = form.address.data
        realty.cost = form.cost.data
        realty.is_sold = form.is_sold.data
        if form.photo.data:
            f = form.photo.data
            filename = secure_filename(f.filename)
            f.save(f'static/img/{filename}')
            realty.photo = f'static/img/{filename}'
        session.add(realty)
        session.commit()
        return redirect('/')
    return render_template('add_realty.html', title='Добавление недвижимости', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.r_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            is_realtor=form.is_realtor.data,
            email=form.email.data,
            phone=form.phone.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/realty_delete/<int:id>")
@login_required
def realty_delete(id):
    session = db_session.create_session()
    realty = session.query(Realties).filter(Realties.id == id, (Realties.realtor == current_user.id) | (current_user.id == 1)).first()
    if realty:
        session.delete(realty)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/edit_realty/<int:id>', methods=["POST", "GET"])
@login_required
def edit_realty(id):
    form = Add_Realty()
    if request.method == 'GET':
        session = db_session.create_session()
        realty = session.query(Realties).filter(Realties.id == id, (Realties.realtor == current_user.id) | (current_user.id == 1)).first()
        user = session.query(User).filter(User.id == realty.realtor).first()
        if realty:
            form.realtor.data = user.name + ' ' + user.surname
            form.house.data = realty.house
            form.not_solded_flats.data = realty.not_solded_flats
            form.address.data = realty.address
            form.cost.data = realty.cost
            form.is_sold.data = realty.is_sold
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        realty = session.query(Realties).filter(Realties.id == id, (Realties.realtor == current_user.id) | (current_user.id == 1)).first()
        if realty:
            n, f = form.realtor.data.split(' ')
            yes = False
            for user in session.query(User).all():
                if user.name == n and user.surname == f:
                    yes = True
                    realty.realtor = user.id
                    break
            if not yes:
                return render_template('add_realty.html',
                                message="Такого риэлтора не сущестсвует",
                                title = "Редактирование недвижимости",
                                form=form)
            realty.house = form.house.data
            realty.not_solded_flats = form.not_solded_flats.data
            realty.address = form.address.data
            realty.cost = form.cost.data
            realty.is_sold = form.is_sold.data
            if form.photo.data:
                f = form.photo.data
                filename = secure_filename(f.filename)
                f.save(f'static/img/{filename}')
                realty.photo = f'static/img/{filename}'
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_realty.html', title='Редактирование недвижимости', form=form)


if __name__ == "__main__":
    db_session.global_init("db/users.sqlite")
    session = db_session.create_session()
    app.run(host='0.0.0.0')