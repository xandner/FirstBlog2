from flask_wtf import FlaskForm
from wtforms import StringField,TextField,TextAreaField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    title=TextField(validators=[DataRequired()])
    slug=TextField(validators=[DataRequired()])
    summary=TextAreaField()
    content=TextAreaField(validators=[DataRequired()])
