from flask import session, render_template, request, abort, jsonify, flash, redirect, url_for
from mod_users.models import User
from mod_users.forms import LoginForm, RegisterForm,ModifyPostForm
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
            flash('user was not found', category='error')
            return render_template('admin/login.html', form=form)

        if not user.check_password(form.password.data):
            flash('incorrect pass', category='error')
            return render_template('admin/login.html', form=form)
        if not user.is_admin():
            flash('you are not admin', category='error')
            return render_template('admin/login.html', form=form)
        session['email'] = user.email
        session['user_id'] = user.id
        session['role'] = user.role
        return redirect(url_for('admin.admin_index'))
    if session.get('role') == 1:
        return redirect(url_for('admin.admin_index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout')
@admin_only_view
def logout():
    session.clear()
    flash('you logged out success fully', 'warning')
    return redirect(url_for('admin.login'))


@admin.route('/posts/new', methods=['GET', 'POST'])
@admin_only_view
def create_post():
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return 'validation on submit error'

        new_post = Post()
        new_post.title = form.title.data
        new_post.content = form.content.data
        new_post.slug = form.slug.data
        new_post.summary = form.summary.data
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('post created')
            return redirect(url_for('admin.admin_index'))
        except IntegrityError:
            db.session.rollback()

    return render_template('admin/create post.html', form=form)


@admin.route('/users', methods=['GET'])
@admin_only_view
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/list_users.html', context=users)


@admin.route('/users/new', methods=['GET'])
@admin_only_view
def get_create_user():
    form = RegisterForm()
    return render_template('admin/new user.html', form=form)


@admin.route('/users/new', methods=['POST'])
@admin_only_view
def post_create_user():
    form = RegisterForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('admin.get_create_user'))
        # return render_template('admin/new user.html', form=form)
    if not form.password.data == form.confirm_password.data:
        msg = 'passwords dosnt match'
        form.password.errors.append(msg)
        form.confirm_password.errors.append(msg)
    new_user = User()
    new_user.fullname = form.full_name.data
    new_user.setPassword(form.password.data)
    new_user.email = form.email.data

    try:
        db.session.add(new_user)
        db.session.commit()
        flash('user was added', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('error.. email used ', 'error')
    return render_template('admin/new user.html', form=form)


@admin.route('/posts')
@admin_only_view
def list_posts():
    posts = Post.query.all()
    return render_template('admin/list_posts.html', posts=posts)


@admin.route('/posts/delete/<int:post_id>')
@admin_only_view
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('post deleted')
    return redirect(url_for('admin.list_posts'))


@admin.route('/posts/<string:slug>')
def single_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return post.title


@admin.route('/posts/modify/<int:post_id>',methods=['GET','POST'])
@admin_only_view
def modify_post(post_id):
    post = Post.query.get_or_404(post_id)
    form=ModifyPostForm(obj=post)
    if request.form=='POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_post.html', form=form, post=post)

        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        try:
            db.session.commit()
            flash('post updated')
        except IntegrityError:
            flash('error')
            db.session.rollback()

    return render_template('admin/modify_post.html',form=form,post=post)
