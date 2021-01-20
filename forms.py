from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=15)])
    submit = SubmitField('STWÓRZ POSTAĆ')


class LoginForm(FlaskForm):
    username = RadioField('Username', validators=[DataRequired(), length(min=2, max=15)])
    submit = SubmitField('Login')
