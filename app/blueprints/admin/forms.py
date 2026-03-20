from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (
  StringField, SubmitField, HiddenField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Length
from app.models import Role


class IDVerificationForm(FlaskForm):
  id = HiddenField('id', validators=[DataRequired()])
  submit = SubmitField(_l('Verify'))


class CreateCategoryForm(FlaskForm):
  name = StringField(_l('name'), validators=[DataRequired(), Length(max=32)])
  submit = SubmitField(_l('Submit'))


class EditCategoryForm(FlaskForm):
  id = HiddenField('id', validators=[DataRequired()])
  name = StringField(_l('name'), validators=[DataRequired(), Length(max=32)])
  submit = SubmitField(_l('Submit'))


class EditUserForm(FlaskForm):
  confirmed = BooleanField(_l('confirmed'))
  role = SelectField('role', coerce=int, validators=[DataRequired()])
  submit = SubmitField(_l('Submit'))
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.role.choices = [(role.id, role.name) for role in Role.query.all()]
