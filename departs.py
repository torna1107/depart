@app.route('/add_depart', methods=['GET', 'POST'])
def add_departament():
    add_form = AddDepartForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department(title=add_form.title.data, chief=add_form.chief.data,
                                members=add_form.members.data, email=add_form.email.data)
        db_sess.add(department)
        db_sess.commit()
        return redirect('/')
    return render_template('add_depart.html', title='Adding a Department', form=add_form)


@app.route("/departments")
def departament():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("departments.html", departments=departments, names=names,
                           title='List of Departments')


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departament(id):
    form = AddDepartForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        depart = db_sess.query(Department).filter(Department.id == id, (Department.chief == current_user.id) | (current_user.id == 1)).first()
        if depart:
            form.title.data = depart.title
            form.chief.data = depart.chief
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = db_sess.query(Department).filter(Department.id == id, (Department.chief == current_user.id) | (current_user.id == 1)).first()
        if depart:
            depart.title = form.title.data
            depart.chief = form.chief.data
            depart.members = form.members.data
            depart.email = form.email.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_depart.html', title='Department Edit', form=form)


@app.route('/depart_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_departament(id):
    db_sess = db_session.create_session()
    depart = db_sess.query(Department).filter(Department.id == id, (Department.chief == current_user.id) | (current_user.id == 1)).first()
    if depart:
        db_sess.delete(depart)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

