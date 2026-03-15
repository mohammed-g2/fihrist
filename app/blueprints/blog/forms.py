from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CreateBlogForm(FlaskForm):
  name = StringField(_l('Blog name'), 
    validators=[DataRequired(), Length(min=3, max=32)])
  description = TextAreaField(_l('Description'), validators=[Length(max=126)])
  submit = SubmitField(_l('Create'))
