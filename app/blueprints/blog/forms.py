import os
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import (
  StringField, BooleanField, SubmitField, TextAreaField, HiddenField,
  SelectField)
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Category


class CreateBlogForm(FlaskForm):
  name = StringField(_l('Blog name'), 
    validators=[DataRequired(), Length(min=3, max=32)])
  description = TextAreaField(_l('Description'), validators=[Length(max=128)])
  submit = SubmitField(_l('Create'))


class CreatePostForm(FlaskForm):
  title = StringField(_l('Title'), validators=[DataRequired(), Length(max=128)])
  image = FileField(
    _l('Image'), 
    validators=[
      FileAllowed(['png', 'jpg'], _l('You can only upload images'))
    ])
  content = TextAreaField(_l('What is on your mind...'))
  category = SelectField(_l('Category'), coerce=int, validators=[DataRequired()])
  submit = SubmitField(_l('Save'))
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.category.choices = [(cat.id, cat.name) for cat in Category.query.all()]
  
  def validate_image(self, field):
    if field.data:
      field.data.seek(0, os.SEEK_END)
      size = field.data.tell()
      field.data.seek(0)
      if size > 2 * 1024 * 1024:
        raise ValidationError('File size must be less than 2MB.')

class IDVerificationForm(FlaskForm):
  id = HiddenField('id', validators=[DataRequired()])
  submit = SubmitField(_l('Verify'))


class CreateCommentForm(FlaskForm):
  post_id = HiddenField('post_id', validators=[DataRequired()])
  content = TextAreaField(
    _l('Content'), validators=[DataRequired(), Length(min=1, max=128)])
  submit = SubmitField(_l('Comment'))
