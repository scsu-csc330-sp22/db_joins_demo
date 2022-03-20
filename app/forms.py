from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddCityForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    population = IntegerField('City Population: ', validators=[DataRequired()])
    country = StringField('Country:', validators=[DataRequired()])
    submit = SubmitField('Save')

class AddCountryForm(FlaskForm):
    country = StringField('Country:', validators=[DataRequired()])
    currency = StringField('Currency: ', validators=[DataRequired()])
    submit = SubmitField('Save')

class DeleteForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Delete')

class SearchForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Search')

class CurrencyForm(FlaskForm):
    currency = StringField('Currency:', validators=[DataRequired()])
    submit = SubmitField('Search for cities')
