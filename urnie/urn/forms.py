from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from wtforms.validators import ValidationError, DataRequired, URL
from flask import current_app


class GoForm(FlaskForm):
    search = StringField("Let's go..", id='urn_autocomplete', validators=[validators.optional(), validators.length(max=200)])
    submit = SubmitField('Go')


class ListUrnsForm(FlaskForm):
    search = StringField('Search on URN or URL..', validators=[validators.optional(), validators.length(max=200)])
    submit = SubmitField('Search')


class AddUriForm(FlaskForm):
    urn = StringField('URN', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')

    def validate_urn(form, field):
        for rule in current_app.url_map.iter_rules():
            print(str(rule))
            if str(rule).endswith('/' + field.data):
                raise ValidationError('URN is reserved and cannot be used.')
