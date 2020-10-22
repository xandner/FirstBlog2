from flask import session, render_template, request, abort, jsonify,flash,redirect,url_for
from mod_users.models import User
from mod_users.forms import LoginForm
from . import admin
from .utils import admin_only_view
from mod_blog.forms import CreatePostForm
from mod_blog.models import Post
from app import db
from sqlalchemy.exc import IntegrityError

@admin.route('/')
@admin_only_view
def admin_index():

    return render_template('admin/index.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        user = User().query.filter(User.email == form.email.data).first()
        if not user:
            flash('user was not found',category='error')
            return render_template('admin/login.html', form=form)

        if not user.check_password(form.password.data):
            flash('incorrect pass',category='error')
            return render_template('admin/login.html', form=form)
        if not user.is_admin():
            flash('you are not admin', category='error')
            return render_template('admin/login.html', form=form)
        session['email'] = user.email
        session['user_id'] = user.id
        session['role'] = user.role
        return redirect(url_for('admin.admin_index'))
    if session.get('role') ==1:
        return redirect(url_for('admin.admin_index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout')
@admin_only_view
def logout():
    session.clear()
    flash('you logged out success fully','warning')
    return redirect(url_for('admin.login'))

@admin.route('/posts/new',methods=['GET','POST'])
@admin_only_view
def create_post():
    form=CreatePostForm(request.form)
    if request.method=='POST':
        if not form.validate_on_submit():
            return 'validation on submit error'

        new_post=Post()
        new_post.title=form.title.data
        new_post.content=form.content.data
        new_post.slug=form.slug.data
        new_post.summary=form.summary.data
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('post created')
            return redirect(url_for('admin.admin_index'))
        except IntegrityError:
            db.session.rollback()


    return render_template('admin/create post.html',form=form)