from flask import render_template, request
from . import blog
from .forms import SearchForm
from .models import Post
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import or_




@blog.route('/')
def index():
    search_form=SearchForm()
    posts = Post.query.all()

    return render_template('blog/index.html', posts=posts,search_form=search_form)


@blog.route('/<string:slug>')
def single_post(slug):
    search_form=SearchForm()
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('blog/single_post.html', post=post,search_form=search_form)


@blog.route('/search')
def search():
    search_form=SearchForm()
    search_query = request.args.get('q', '')
    title_cond = Post.title.ilike(f'%{search_query}%')
    summary_cond = Post.summary.ilike(f'%{search_query}%')
    content_cond = Post.content.ilike(f'%{search_query}%')
    found_posts = Post.query.filter(
        or_(
            title_cond,
            summary_cond,
            content_cond
        )
    ).all()
    print(found_posts)
    return render_template('blog/search.html', posts=found_posts, search_form=search_form)
