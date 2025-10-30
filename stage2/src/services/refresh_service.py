import requests
from datetime import datetime
from random import randint
from sqlalchemy import func
from ..models import Country, Meta
from ..database import db
from ..utils.image_generator import generate_summary_image

COUNTRIES_API = 'https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies'
RATES_API = 'https://open.er-api.com/v6/latest/USD'

class ExternalAPIError(Exception):
    pass

def validate_country_payload(country):
    errors = {}

    if not country.get('name'):
        errors['name'] = 'is required'
    if country.get('population') is None:
        errors['population'] = 'is required'

    currencies = country.get('currencies')
    currency_code = pick_currency_code(currencies)
    if not currency_code:
        errors['currency_code'] = 'is required'

    return errors

def pick_currency_code(currencies):
    if not currencies or not isinstance(currencies, list) or len(currencies) == 0:
        return None
    first = currencies[0]
    return first.get('code') if isinstance(first, dict) else None

def compute_estimated_gdp(population, exchange_rate) -> float | None:
    if exchange_rate is None:
        return None
    multiplier = randint(1000, 2000)
    return (population * multiplier) / exchange_rate

def refresh_all(timeout_seconds=30):
    try:
        response1 = requests.get(COUNTRIES_API, timeout=timeout_seconds)
        response1.raise_for_status()
    except Exception:
        raise ExternalAPIError('Could not fetch data from Countries API')

    try:
        response2 = requests.get(RATES_API, timeout=timeout_seconds)
        response2.raise_for_status()
    except Exception:
        raise ExternalAPIError('Could not fetch data from Exchange Rates API')

    countries = response1.json()
    rates = response2.json().get('rates', {}) if isinstance(response2.json(), dict) else {}
    now = datetime.now()

    session = db.session()
    try:
        for country in countries:
            name = country.get('name')
            population = country.get('population')
            capital = country.get('capital')
            region = country.get('region')
            flag = country.get('flag')
            currencies = country.get('currencies')
            currency_code = pick_currency_code(currencies)

            if not currencies or len(currencies) == 0:
                currency_code = None
                exchange_rate = None
                estimated_gdp = 0

            elif currency_code not in rates:
                exchange_rate = None
                estimated_gdp = None

            else:
                exchange_rate = rates[currency_code]
                estimated_gdp = compute_estimated_gdp(population, exchange_rate)

            existing = session.query(Country).filter(
                func.lower(Country.name) == name.lower()
            ).one_or_none()

            if existing:
                existing.capital = capital
                existing.region = region
                existing.population = population
                existing.currency_code = currency_code
                existing.exchange_rate = exchange_rate
                existing.estimated_gdp = estimated_gdp
                existing.flag_url = flag
                existing.last_refreshed_at = now
                session.add(existing)
            else:
                new = Country(
                    name=name,
                    capital=capital,
                    region=region,
                    population=population,
                    currency_code=currency_code,
                    exchange_rate=exchange_rate,
                    estimated_gdp=estimated_gdp,
                    flag_url=flag,
                    last_refreshed_at=now,
                )
                session.add(new)
        session.commit()

        # After commit generate image
        total = session.query(Country).count()
        top5_q = session.query(Country).filter(Country.estimated_gdp is not None).order_by(
            Country.estimated_gdp.desc()).limit(5).all()
        top5 = [{'name': c.name, 'estimated_gdp': c.estimated_gdp} for c in top5_q]

        image_path = generate_summary_image(total, top5, now)

        # Update Meta table
        meta = session.query(Meta).filter(Meta.key == 'last_refreshed_at').one_or_none()
        if meta:
            meta.value = now.isoformat()
        else:
            meta = Meta(key='last_refreshed_at', value=now.isoformat())
            session.add(meta)
        session.commit()

        return {'total': total, 'last_refreshed_at': now.isoformat(), 'image_path': image_path}
    except ExternalAPIError:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
