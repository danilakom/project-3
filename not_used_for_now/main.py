@app.route('/departaments')
def departaments():
    deps = session.query(Departament)
    chief = {}
    for dep in deps:
        user = session.query(User).filter(User.id == dep.chief).first()
        if user:
            chief[dep.id] = ' '.join([user.name, user.surname])
        else:
            chief[dep.id] = ''
    return render_template('departaments.html', departaments=deps, chief=chief)


@app.route('/add_departament', methods=['GET', 'POST'])
@login_required
def add_departament():
    form = Add_Departament()
    if form.validate_on_submit():
        session = db_session.create_session()
        dep = Departament()
        a = [user.id for user in session.query(User)]
        if form.chief.data not in a:
            return render_template('add_departament.html',
                               message="Такого пользователя не сущестсвует",
                               form=form)
        dep.chief = form.chief.data
        dep.title = form.title.data
        dep.members = form.members.data
        dep.email = form.email.data
        session.add(dep)
        session.commit()
        return redirect('/departaments')
    return render_template('add_departament.html', title='Добавление департамента', form=form)


@app.route("/departament_delete/<int:id>")
@login_required
def departament_delete(id):
    session = db_session.create_session()
    dep = session.query(Departament).filter(Departament.id == id, (Departament.chief == current_user.id) | (current_user.id == 1)).first()
    if dep:
        session.delete(dep)
        session.commit()
    else:
        abort(404)
    return redirect('/departaments')


@app.route('/edit_departament/<int:id>', methods=["POST", "GET"])
@login_required
def edit_departament(id):
    form = Add_Departament()
    if request.method == 'GET':
        session = db_session.create_session()
        dep = session.query(Departament).filter(Departament.id == id, (Departament.chief == current_user.id) | (current_user.id == 1)).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        dep = session.query(Departament).filter(Departament.id == id, (Departament.chief == current_user.id) | (current_user.id == 1)).first()
        if dep:
            dep.chief = form.chief.data
            dep.title = form.title.data
            dep.members = form.members.data
            dep.email = form.email.data
            session.commit()
            return redirect('/departaments')
        else:
            abort(404)
    return render_template('add_departament.html', title='Редактирование департамента', form=form)