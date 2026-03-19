from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (
  StringField, SubmitField, HiddenField)
from wtforms.validators import DataRequired, Length


class IDVerificationForm(FlaskForm):
  id = HiddenField('id', validators=[DataRequired()])
  submit = SubmitField(_l('Verify'))


class CreateCategoryForm(FlaskForm):
  name = StringField('name', validators=[DataRequired(), Length(max=32)])
  submit = SubmitField(_l('Submit'))


class EditCategoryForm(FlaskForm):
  id = HiddenField('id', validators=[DataRequired()])
  name = StringField('name', validators=[DataRequired(), Length(max=32)])
  submit = SubmitField(_l('Submit'))
