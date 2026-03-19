from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (
  StringField, BooleanField, SubmitField, TextAreaField, HiddenField,
  SelectField)
from wtforms.validators import DataRequired, Length
from app.models import Category


class CreateBlogForm(FlaskForm):
  name = StringField(_l('Blog name'), 
    validators=[DataRequired(), Length(min=3, max=32)])
  description = TextAreaField(_l('Description'), validators=[Length(max=128)])
  submit = SubmitField(_l('Create'))


class CreatePostForm(FlaskForm):
  title = StringField(_l('Title'), validators=[DataRequired(), Length(max=128)])
  content = TextAreaField(_l('What is on your mind...'))
  category = SelectField(_l('Category'), coerce=int, validators=[DataRequired()])
  submit = SubmitField(_l('Save'))
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.category.choices = [(cat.id, cat.name) for cat in Category.query.all()]


class IDVerificationForm(FlaskForm):
  id = HiddenField('id', validators=[DataRequired()])
  submit = SubmitField(_l('Verify'))


class CreateCommentForm(FlaskForm):
  post_id = HiddenField('post_id', validators=[DataRequired()])
  content = TextAreaField(
    _l('Content'), validators=[DataRequired(), Length(min=1, max=128)])
  submit = SubmitField(_l('Comment'))
