from app import db


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(64), index=True, unique=True)
    currency = db.Column(db.String(32), index=False, unique=False)
    cities = db.relationship('City', backref='country', lazy='dynamic')

    def __repr__(self):
        return '{} {}'.format(self.country, self.currency)

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64), unique=False, index=True)
    population = db.Column(db.Integer, unique=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

    def __repr__(self):
        return '{} {}'.format(self.city, self.population)
