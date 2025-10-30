from .database import db
from datetime import datetime, timezone


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    capital = db.Column(db.String(128))
    region = db.Column(db.String(64))
    population = db.Column(db.BigInteger)
    currency_code = db.Column(db.String(8), nullable=True)
    exchange_rate = db.Column(db.Float, nullable=True)
    estimated_gdp = db.Column(db.Float, nullable=True)
    flag_url = db.Column(db.String(255))
    last_refreshed_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Meta(db.Model):
    __tablename__ = 'meta'

    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text)
