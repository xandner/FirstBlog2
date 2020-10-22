from app import db

posts_categories = db.Table('posts_category', db.metadata,
                          db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='cascade')),
                          db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete='cascade'))
                          )


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(68), nullable=False, unique=True)
    description = db.Column(db.String(256))
    slug = db.Column(db.String(256), unique=True)
    posts=db.relationship('Post',secondary=posts_categories)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(68), nullable=False, unique=True)
    summary = db.Column(db.String(256))
    content = db.Column(db.TEXT, nullable=False)
    slug = db.Column(db.String(256), unique=True)
    category = db.relationship('Category', secondary=posts_categories)
