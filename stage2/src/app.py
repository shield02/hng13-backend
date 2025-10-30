import os
from flask import Flask, request, jsonify, send_file
from sqlalchemy import func
from .config import Config
from .database import db
from .models import Country, Meta
from .services.refresh_service import refresh_all, ExternalAPIError

def create_app(config: Config):
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        # create tables if they don't exist
        db.create_all()

    @app.route('/')
    def home():
        return "Welcome to Countries Currency Exchange App"

    @app.route('/countries/refresh', methods=['POST'])
    def refresh():
        try:
            result = refresh_all(timeout_seconds=Config.REFRESH_TIMEOUT_SECONDS)

            if isinstance(result, tuple):
                data, status = result
            else:
                data, status = result, 200

            if "error" in data:
                return jsonify(data), status

            return jsonify({
                'message': 'Refresh Completed',
                'total_countries': data['total'],
                'last_refreshed_at': data['last_refreshed_at'],
            })
        except ExternalAPIError as e:
            return jsonify({
                'error': 'External data source unavailable',
                'details': str(e)}
            ), 503
        except Exception as e:
            app.logger.exception('Refresh failed')
            return jsonify({'error': f'Internal server error: {e}'}), 500

    @app.route('/countries', methods=['GET'])
    def countries():
        region = request.args.get('region')
        currency = request.args.get('currency')
        sort = request.args.get('sort')

        query = Country.query

        if region:
            query = query.filter(Country.region == region)
        if currency:
            query = query.filter(Country.currency_code == currency)

        if sort == 'gdp_desc':
            query = query.order_by(Country.estimated_gdp.desc())
        elif sort == 'gdp_asc':
            query = query.order_by(Country.estimated_gdp.asc())

        all_countries = query.all()

        return jsonify([
            {
                "id": c.id,
                "name": c.name,
                "capital": c.capital,
                "region": c.region,
                "population": c.population,
                "currency_code": c.currency_code,
                "exchange_rate": c.exchange_rate,
                "estimated_gdp": c.estimated_gdp,
                "flag_url": c.flag_url,
                "last_refreshed_at": c.last_refreshed_at.isoformat() if c.last_refreshed_at else None
            }
            for c in all_countries
        ])

    @app.route('/countries/<name>', methods=['GET'])
    def get_country(name):
        country = Country.query.filter(Country.name.ilike(name)).first()
        if not country:
            return jsonify({'error': 'Country not found'}), 404

        return jsonify({
            'id': country.id,
            'name': country.name,
            'capital': country.capital,
            'region': country.region,
            'currency_code': country.currency_code,
            'exchange_rate': country.exchange_rate,
            'estimated_gdp': country.estimated_gdp,
            'flag_url': country.flag_url,
            'last_refreshed_at': country.last_refreshed_at,
        })

    @app.route('/countries/image', methods=['GET'])
    def country_image():
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, 'cache', 'summary.png')
            file_path = os.path.abspath(file_path)

            if not os.path.exists(file_path):
                return jsonify({
                    'error': 'Summary image not found'
                }), 404

            return send_file(file_path, mimetype='image/png', max_age=0)
        except Exception as e:
            app.logger.error(f"Error sending image: {e}")
            return jsonify({'error': 'Could not send image'}), 500

    @app.route('/status', methods=['GET'])
    def status():
        total_countries = db.session.query(func.count(Country.id)).scalar()

        # Latest refresh timestamp based on the most recently updated country
        last_refresh = db.session.query(
            func.max(Country.last_refreshed_at)
        ).scalar()

        return jsonify({
            "total_countries": total_countries,
            "last_refreshed_at": last_refresh.isoformat() + "Z" if last_refresh else None
        })

    @app.route('/countries/<string:name>', methods=['DELETE'])
    def delete_country(name):
        # Case-insensitive match
        country = Country.query.filter(
            func.lower(Country.name) == name.lower()
        ).first()

        if not country:
            return jsonify({"error": f'Country "{name}" not found'}), 404

        try:
            db.session.delete(country)
            db.session.commit()
            return jsonify({"message": f"{country.name} removed successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Internal server error"}), 500

    return app
