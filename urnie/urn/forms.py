from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, URL, Length


class ListUrnsForm(FlaskForm):
    search = StringField('Search on URN or URL..', [validators.optional(), validators.length(max=200)])
    submit = SubmitField('Search')


class AddUriForm(FlaskForm):
    urn = StringField('URN', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')
