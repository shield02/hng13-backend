from database import db

class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    capital = db.Column(db.String(255), nullable=True)
    region = db.Column(db.String, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    currency_code = db.Column(db.String(10), nullable=True)
    exchange_rate = db.Column(db.Float, nullable=True)
    estimated_gdp = db.Column(db.Float, nullable=True)
    flag_url = db.Column(db.Text, nullable=True)
    last_refreshed_at = db.Column(db.DateTime, nullable=True)

class Meta(db.Model):
    __tablename__ = "meta"
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text)
