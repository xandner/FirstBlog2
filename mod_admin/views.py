from flask import session, render_template, request, abort, jsonify
from mod_users.models import User
from mod_users.forms import LoginForm
from . import admin


@admin.route('/')
def admin_index():
    return 'hello admin'


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        user = User().query.filter(User.email == form.email.data).first()
        if not user:
            abort(400)

        if not user.check_password(form.password.data):
            return 'incorrect password', 400
        session['email'] = user.email
        return 'logged in'
    if session.get('email') is not None:
        return 'sessions logged in'
    return render_template('admin/login.html', form=form)
