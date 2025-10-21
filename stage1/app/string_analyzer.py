from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
import hashlib

from utils.compute_properties import compute_properties
from utils.parse_natural_language import parse_natural_language

string_bp = Blueprint("strings", __name__)

# In-memory storage: {sha256_hash: record}
STRING_STORE = {}


@string_bp.route("/strings", methods=["POST"])
def create_string():
    """This a post-request.

    Analyze and store a string
    """
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 400

    body = request.get_json()
    if not body or "value" not in body:
        return jsonify({"error": "Missing 'value' field"}), 400

    value = body["value"]
    if not isinstance(value, str):
        return jsonify({"error": "'value' must be a string"}), 422

    props = compute_properties(value)
    string_id = props["sha256_hash"]

    if string_id in STRING_STORE:
        return jsonify({"error": "String already exists"}), 409

    record = {
        "id": string_id,
        "value": value,
        "properties": props,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    STRING_STORE[string_id] = record

    return jsonify(record), 201


@string_bp.route("/strings/<string_value>", methods=["GET"])
def get_string(string_value):
    """A GET request.

    Checks if a string exists.

    Returns:
        jsonify(dist) 200: On success
    """
    hash_val = hashlib.sha256(string_value.encode()).hexdigest()
    try:
        record = STRING_STORE.get(hash_val)
    except Exception as e:
        return jsonify({"error": f"String does not exist: {e}"}), 404

    if not record:
        return jsonify({"error": "String not found"}), 404

    return jsonify(record), 200


@string_bp.route("/strings", methods=["GET"])
def list_strings():
    """A GET request.

     Get all strings with filtering using query params.

     Returns:
         jsonify(dict) 200: On success.
     """
    filters = {
        "is_palindrome": request.args.get("is_palindrome"),
        "min_length": request.args.get("min_length", type=int),
        "max_length": request.args.get("max_length", type=int),
        "word_count": request.args.get("word_count", type=int),
        "contains_character": request.args.get("contains_character"),
    }

    results = list(STRING_STORE.values())

    try:
        if filters["is_palindrome"] is not None:
            val = filters["is_palindrome"].lower() in ("true", "false")
            results = [r for r in results if r["properties"]["is_palindrome"] == val]

        if filters["min_length"] is not None:
            results = [r for r in results if r["properties"]["length"] >= filters["min_length"]]

        if filters["max_length"] is not None:
            results = [r for r in results if r["properties"]["length"] <= filters["max_length"]]

        if filters["word_count"] is not None:
            results = [r for r in results if r["properties"]["word_count"] == filters["word_count"]]

        if filters["contains_character"]:
            char = filters["contains_character"]
            results = [r for r in results if char in r["value"]]

    except Exception as e:
        return jsonify({"error": f"Invalid query parameters: {e}"}), 400

    return jsonify({
        "data": results,
        "count": len(results),
        "filters_applied": {k: v for k, v in filters.items() if v is not None},
    }), 200


@string_bp.route("/strings/filter-by-natural-language", methods=["GET"])
def filter_by_natural_language():
    """A GET request.

    Get all strings with filtering using natural language.

    Exception:
        BadRequest (400): Unable to parse the query.
        Unprocessable (422): Unable to parse the query.

    Returns:
        jsonify response (200): On successful response.
    """
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    filters = parse_natural_language(query)
    if not filters:
        return jsonify({"error": "Unable to parse natural language query"}), 400

    # Reuse filtering logic
    results = list(STRING_STORE.values())
    if "is_palindrome" in filters:
        results = [r for r in results if r["properties"]["is_palindrome"]]
    if "word_count" in filters:
        results = [r for r in results if r["properties"]["word_count"] == filters["word_count"]]
    if "min_length" in filters:
        results = [r for r in results if r["properties"]["length"] >= filters["min_length"]]
    if "contains_character" in filters:
        results = [r for r in results if filters["contains_character"] in r["value"]]

    return jsonify({
        "data": results,
        "count": len(results),
        "interpreted_query": {
            "original": query,
            "parsed_filters": filters,
        }
    }), 200


@string_bp.route("/strings/<string_value>", methods=["DELETE"])
def delete_string(string_value):
    """A DELETE request.

    Exception:
        Not Found (404): When resource not found.

    Returns:
        jsonify response (200): On successful response.
    """
    hash_val = hashlib.sha256(string_value.encode()).hexdigest()

    if hash_val not in STRING_STORE:
        return jsonify({"error": "String not found"}), 404
    del STRING_STORE[hash_val]

    return "", 204
