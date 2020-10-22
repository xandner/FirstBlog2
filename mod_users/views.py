from flask import request, render_template,flash
from app import db

from . import users
from .forms import RegisterForm
from .models import User


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('users/register.html', form=form)
        if not form.password.data == form.confirm_password.data:
            msg='passwords dosnt match'
            form.password.errors.append(msg)
            form.confirm_password.errors.append(msg)
        new_user=User()
        new_user.fullname=form.full_name.data
        new_user.setPassword(form.password.data)
        new_user.email=form.email.data
        db.session.add(new_user)
        db.session.commit()
        flash('user was added','success')



    return render_template('users/register.html', form=form)
