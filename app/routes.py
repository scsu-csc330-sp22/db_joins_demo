from app import app
from flask import render_template, redirect, url_for
from app.forms import AddCountryForm, AddCityForm, DeleteForm, SearchForm, CurrencyForm
from app import db
from app.models import City, Country
import sys

@app.route('/')
def hello():
    return render_template('homepage.html')

@app.route('/add_country', methods=['GET', 'POST'])
def add_country():
    form = AddCountryForm()
    if form.validate_on_submit():
        # Extract values from form
        country_name = form.country.data
        currency = form.currency.data
        print(country_name, currency, file=sys.stderr)

        # Create a city record to store in the DB
        c = Country(country=country_name, currency=currency)

        # add record to table and commit changes
        db.session.add(c)
        db.session.commit()

        form.country.data = ''
        form.currency.data = ''
        return redirect(url_for('view_countries'))
    return render_template('add_country.html', form=form)

@app.route('/view_countries')
def view_countries():
    all = db.session.query(Country).all()
    print(all, file=sys.stderr)
    return render_template('view_countries.html', countries=all)


@app.route('/add_city', methods=['GET', 'POST'])
def add_record():
    form = AddCityForm()
    if form.validate_on_submit():
        # Extract values from form
        city_name = form.city.data
        population = form.population.data
        country = form.country.data

        country_obj = db.session.query(Country).filter_by(
            country = country).first()

        print(country_obj, file=sys.stderr)
        # Create a city record to store in the DB
        c = City(city=city_name, population=population, country=country_obj)

        # add record to table and commit changes
        db.session.add(c)
        db.session.commit()

        form.city.data = ''
        form.population.data = ''
        return redirect(url_for('view_cities'))
    return render_template('add_city.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete_record():
    form = DeleteForm()
    if form.validate_on_submit():
        # Query DB for matching record (we'll grab the first record in case
        # there's more than one).
        to_delete = db.session.query(City).filter_by(city = form.city.data).first()

        # If record is found delete from DB table and commit changes
        if to_delete is not None:
            db.session.delete(to_delete)
            db.session.commit()

        form.city.data = ''
        # Redirect to the view_all route (view function)
        return redirect(url_for('view_cities'))
    return render_template('delete.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search_by_name():
    form = SearchForm()
    if form.validate_on_submit():
        # Query DB table for matching name
        record = db.session.query(City).filter_by(city = form.city.data).all()
        if record:
            return render_template('view_cities.html', cities=record)
        else:
            return render_template('not_found.html')
    return render_template('search.html', form=form)

@app.route('/view_cities')
def view_cities():
    all = db.session.query(City).all()
    print(all, file=sys.stderr)
    return render_template('view_cities.html', cities=all)

@app.route('/sort_by_name')
def sort_by_name():
    all = db.session.query(City).order_by(City.city).all()
    print(all, file=sys.stderr)
    return render_template('view_cities.html', cities=all)

@app.route('/filter_currency', methods=['GET', 'POST'])
def filter_currency():
    form = CurrencyForm()
    if form.validate_on_submit():
        currency = form.currency.data
        # Execute query and store result in list of tuples
        results = db.session.query(City.city, Country.currency).join(
            City).filter(Country.currency==currency).all()

        # Show results in terminal
        print(results, file=sys.stderr)

        if results:
            return render_template('view_city_currency.html', cities=results)
        else:
            return render_template('not_found.html')
    return render_template('currency.html', form=form)

@app.route('/delete_db')
def delete_db():
    db.drop_all()
    db.create_all()
    return render_template('delete_db.html')
