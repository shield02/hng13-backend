import os

from flask import Flask, jsonify
import requests

from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/')
@app.route('/me', methods=['GET'])
def me():
    """Get a dynamic cat fact from external API with profile information

    The endpoint returns JSON data

    Exception:
        Returns an exception
    Returns:
        JSON data
    """
    headers = {
        'Accept': 'application/json',
    }
    fact = "Cats are amazing creatures!"

    try:
        response = requests.get(
            "https://catfact.ninja/fact",
            headers=headers,
            timeout=5
        )

        if response.ok:
            fact = response.json().get("fact", fact)
        else:
            app.logger.warning(
                f"Cat Facts API returned bad status: "
                f"{getattr(response, 'status_code', 'N/A')}"
            )
    except Exception as e:
        app.logger.error(f"Failed to fetch cat fact: {e}")
        fact = "Couldn't fetch cats facts."

    data = {
        "status": "success",
        "user": {
            "email": "myshield02@email.com",
            "name": "Otuekong Enang",
            "stack": "Python/Flask",
        },
        "timestamp": (datetime
                      .now(timezone.utc)
                      .isoformat()
                      .replace("+00:00", "Z")
                      ),
        "fact": fact,
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000))
    )
