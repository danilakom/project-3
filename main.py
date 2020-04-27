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
sort = ''

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/', methods=['GET', 'POST'])
def index():
    global sort
    if request.method == 'GET':
        if sort:
            if sort == 'name-up':
                realties = session.query(Realties).order_by(Realties.id)
            elif sort == 'name-down':
                realties = session.query(Realties).order_by(Realties.id)[::-1]
            elif sort == 'cost-up':
                realties = session.query(Realties).order_by(Realties.cost)
            elif sort == 'cost-down':
                realties = session.query(Realties).order_by(Realties.cost)[::-1]
        else:
            realties = session.query(Realties)
        realtor = {}
        for realty in realties:
            user = session.query(User).filter(User.id == realty.realtor).first()
            if user:
                realtor[realty.id] = ' '.join([user.name, user.surname])
            else:
                realtor[realty.id] = ''
        return render_template('index.html', realties=realties, realtor=realtor, title='Квартиры')
    elif request.method == 'POST':
        sort = f'{request.form["sort-by"]}-{request.form["sort"]}'
        return redirect('/')


@app.route('/realty/<int:id>')
def realty(id):
    realty = session.query(Realties).filter(Realties.id == id).first()
    user = session.query(User).filter(User.id == realty.realtor).first()
    if user:
        r = ' '.join([user.name, user.surname])
        e = user.email
        p = user.phone
    if realty.photo:
        files = realty.photo.split(',')
    else:
        files = ''
    return render_template('realty.html', realty=realty, realtor=r, files=files, email=e, phone=p)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        try:
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            else:
                return render_template('login.html',
                                message="Неправильный логин или пароль",
                                title="Авторизация",
                                form=form)
        except AttributeError:
            return render_template('login.html',
                                message="Неправильный логин или пароль",
                                title="Авторизация",
                                form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

@app.route('/user/<int:id>')
@login_required
def show_user(id):
    user = session.query(User).filter(User.id == id).first()
    return render_template('show_user.html', title="Личный кабинет", user=user)

@app.route('/change_user/<int:id>', methods=["POST", "GET"])
def change_user(id):
    form = RegisterForm()
    if request.method == 'GET':
        user = session.query(User).filter(User.id == id).first()
        if user:
            form.surname.data = user.surname
            form.name.data = user.name
            form.age.data = user.age
            form.is_realtor.data = user.is_realtor
            form.email.data = user.email
            form.phone.data = user.phone
        else:
            abort(404)
    if form.validate_on_submit():
        user = session.query(User).filter(User.id == id).first()
        if user:
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.is_realtor = form.is_realtor.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.set_password(form.password.data)
            return redirect('/')
        else:
            abort(404)
    return render_template('/register.html', title="Редактирование пользователя", form=form)


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
            if user.name.lower() == n.lower() and user.surname.lower() == f.lower():
                yes = True
                realty.realtor = user.id
                break
        if not yes:
            return render_template('add_realty.html',
                               message="Такого риэлтора не сущестсвует",
                               title="Добавить дом",
                               form=form)
        realty.house = form.house.data
        realty.desc = form.desc.data
        realty.address = form.address.data
        k = 0
        cost = ''
        for i in list(str(form.cost.data))[::-1]:
            if k == 3:
                cost += ' '
                cost += i
                k = 1
            else:
                cost += i
                k += 1
        realty.cost = cost[::-1]
        if form.photo.data[0].filename != '':
            p = []
            for i in form.photo.data:
                f = i
                filename = secure_filename(f.filename)
                if filename != '':
                    f.save(f'static/img/{filename}')
                    p.append(filename)
            realty.photo = ','.join(p)
        session.add(realty)
        session.commit()
        return redirect('/')
    return render_template('add_realty.html', title='Добавить дом', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким email уже есть!")
        if session.query(User).filter(User.phone == form.phone.data).first():
            if form.phone.data:
                return render_template('register.html', title="Регистрация", form=form,
                                        message="Пользователь с таким номером телефона уже есть!")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            is_realtor=form.is_realtor.data,
            email=form.email.data)
        if form.phone.data:
            user.phone = form.phone.data
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
            form.house.data = True if realty.house == 0 else False
            form.desc.data = realty.desc
            form.address.data = realty.address
            form.cost.data = ''.join(realty.cost.split(' '))
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        realty = session.query(Realties).filter(Realties.id == id, (Realties.realtor == current_user.id) | (current_user.id == 1)).first()
        if realty:
            n, f = form.realtor.data.split(' ')
            yes = False
            for user in session.query(User).all():
                if user.name.lower() == n.lower() and user.surname.lower() == f.lower():
                    yes = True
                    realty.realtor = user.id
                    break
            if not yes:
                return render_template('add_realty.html',
                                message="Такого риэлтора не сущестсвует",
                                title = "Редактирование дома",
                                form=form)
            realty.house = form.house.data
            realty.address = form.address.data
            k = 0
            cost = ''
            for i in list(str(form.cost.data))[::-1]:
                if k == 3:
                    cost += ' '
                    cost += i
                    k = 1
                else:
                    cost += i
                    k += 1
            realty.cost = cost[::-1]
            if form.photo.data[0].filename != '':
                p = []
                for i in form.photo.data:
                    f = i
                    filename = secure_filename(f.filename)
                    if filename != '':
                        f.save(f'static/img/{filename}')
                        p.append(filename)
                realty.photo = ','.join(p)
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_realty.html', title='Редактирование дома', form=form)


if __name__ == "__main__":
    db_session.global_init("db/users.sqlite")
    session = db_session.create_session()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)