from .database import db
from datetime import datetime, timezone


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    capital = db.Column(db.String(128))
    region = db.Column(db.String(64))
    population = db.Column(db.BigInteger)
    currency_code = db.Column(db.String(8), nullable=False)
    exchange_rate = db.Column(db.Float)
    estimated_gdp = db.Column(db.Float)
    flag_url = db.Column(db.String(255))
    last_refreshed_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Meta(db.Model):
    __tablename__ = 'meta'

    id = db.Column(db.Integer, primary_key=True)
    last_refreshed_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
