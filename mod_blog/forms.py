from flask_wtf import FlaskForm
from wtforms import StringField, TextField, TextAreaField
from wtforms.validators import DataRequired

from utils.forms import SelectMultiCheckboxField


class CreatePostForm(FlaskForm):
    title = TextField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])


class CategoryForm(FlaskForm):
    name = TextField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    description = TextAreaField()
class PostForm(FlaskForm):
    title = TextField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])
    categories = SelectMultiCheckboxField(coerce=int)


class SearchForm(FlaskForm):
    search_query=TextField(validators=[DataRequired()])

