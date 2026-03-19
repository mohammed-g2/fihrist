from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (
  StringField, BooleanField, SubmitField, TextAreaField, HiddenField)
from wtforms.validators import DataRequired, Length


class IDVerificationForm(FlaskForm):
  id = HiddenField('id', validators=[DataRequired()])
  submit = SubmitField(_l('Verify'))
