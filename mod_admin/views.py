from flask import session, render_template, request, abort, jsonify, flash, redirect, url_for
from mod_users.models import User
from mod_users.forms import LoginForm, RegisterForm
from . import admin
from .utils import admin_only_view
from mod_blog.forms import CreatePostForm, CategoryForm, PostForm
from mod_blog.models import Post, Category
from app import db
from sqlalchemy.exc import IntegrityError
from mod_uploads.forms import FileUploadForm
from mod_uploads.models import File
from werkzeug.utils import secure_filename
import uuid


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
    form = PostForm(request.form)
    categories = Category.query.all()
    form.categories.choices = [(category.id, category.name) for category in categories]

    if request.method == 'POST':
        if not form.validate_on_submit():
            return 'validation on submit error'

        new_post = Post()
        new_post.title = form.title.data
        new_post.content = form.content.data
        new_post.slug = form.slug.data
        new_post.summary = form.summary.data
        new_post.category = [Category.query.get(category_id) for category_id in form.categories.data]
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


@admin.route('/posts/modify/<int:post_id>', methods=['GET', 'POST'])
@admin_only_view
def modify_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    categories = Category.query.all()
    form.categories.choices = [(category.id, category.name) for category in categories]
    if request.method != 'POST':
        form.categories.data = [category.id for category in post.category]
    if request.form == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_post.html', form=form, post=post)

        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        post.category = form.categories.choices = [(category.id, category.name) for category in categories]
        try:
            db.session.commit()
            flash('post updated')
        except IntegrityError:
            flash('error')
            db.session.rollback()

    return render_template('admin/modify_post.html', form=form, post=post)


@admin.route('/category/new', methods=['GET', 'POST'])
@admin_only_view
def create_category():
    form = CategoryForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return 'validation on submit error'

        new_category = Category()
        new_category.name = form.name.data
        new_category.slug = form.slug.data
        new_category.description = form.description.data
        try:
            db.session.add(new_category)
            db.session.commit()
            flash('category created')
            return redirect(url_for('admin.admin_index'))
        except IntegrityError:
            db.session.rollback()
            flash('error')
            return render_template('admin/create_category.html', form=form)

    return render_template('admin/create_category.html', form=form)


@admin.route('/categories')
@admin_only_view
def list_categories():
    categories = Category.query.all()
    return render_template('admin/list_categories.html', categories=categories)


@admin.route('/category/<string:name>')
def single_category(name):
    category = Category.query.filter(Category.name == name).first_or_404()
    return category.name


@admin.route('/category/delete/<int:category_id>')
@admin_only_view
def delete_category(category_id):
    cat = Category.query.get_or_404(category_id)
    db.session.delete(cat)
    db.session.commit()
    flash('category deleted')
    return redirect(url_for('admin.list_categories'))


@admin.route('/category/modify/<int:category_id>', methods=['GET', 'POST'])
@admin_only_view
def modify_category(category_id):
    cat = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=cat)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_category.html', form=form, category=cat)
        cat.name = form.name.data
        cat.description = form.description.data
        cat.description = form.description.data
        cat.slug = form.slug.data
        try:
            db.session.commit()
            flash('category updated ')
        except IntegrityError:
            db.session.rollback()
            flash('error')
    return render_template('admin/modify_category.html', form=form, category=cat)


@admin.route('library/upload', methods=['GET', 'POST'])
@admin_only_view
def upload_file():
    form = FileUploadForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return '1'
        file_name = f'{uuid.uuid1()}_{secure_filename(form.file.data.filename)}'
        new_file = File()
        new_file.file_name = file_name
        try:
            db.session.add(new_file)
            db.session.commit()
            form.file.data.save(f'static/uploads/{file_name}')
            flash(f'file uploaded on {url_for("static", file_name="uploads/"+file_name)}')
            print(f'file uploaded on {url_for("static", file_name="uploads/"+file_name)}')
        except Exception:
            db.session.rollback()
            return str(Exception)

    return render_template('admin/upload_file.html', form=form)
