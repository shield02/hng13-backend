import httpx
from typing import Optional, List, Dict
from ..core.config import settings

# Nominatim + Overpass API endpoints
NOMINATIM_SEARCH = "https://nominatim.openstreetmap.org/search"
OVERPASS_API = "https://overpass-api.de/api/interpreter"


# ----------------------------------------------------------
# NOMINATIM — get coordinates for a city or location name
# ----------------------------------------------------------
async def nominatim_geocode(query: str) -> Optional[Dict]:
    """
    Geocode a place name (e.g., 'Lagos') using OpenStreetMap's Nominatim API.
    Returns first match: {'lat': ..., 'lon': ..., 'display_name': ...}
    """
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "Eco-Mind/1.0 (contact@example.com)"}

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(NOMINATIM_SEARCH, params=params, headers=headers)
            r.raise_for_status()
            data = r.json()
            if not data:
                return None
            return data[0]
        except Exception as e:
            print(f"[nominatim_geocode] Error: {e}")
            return None


# ----------------------------------------------------------------
# OVERPASS — find recycling / waste facilities near coordinates
# ----------------------------------------------------------------
async def overpass_recycling_near(
        lat: float,
        lon: float,
        radius_m: int = 5000,
        material: Optional[str] = None
) -> List[Dict]:
    """
    Search OpenStreetMap for recycling or waste-disposal facilities near the given coordinates.
    Can optionally filter by material type (plastic, glass, metal, etc.).
    """

    # Build an Overpass query dynamically
    material_filters = ""
    if material:
        material = material.lower()
        if material in ["plastic", "glass", "paper", "metal", "electronics", "battery"]:
            material_filters = f"""
            node(around:{radius_m},{lat},{lon})[recycling:{material}=yes];
            way(around:{radius_m},{lat},{lon})[recycling:{material}=yes];
            """

    query = f"""
    [out:json][timeout:25];
    (
      node(around:{radius_m},{lat},{lon})[amenity=recycling];
      way(around:{radius_m},{lat},{lon})[amenity=recycling];
      node(around:{radius_m},{lat},{lon})[waste_disposal=yes];
      way(around:{radius_m},{lat},{lon})[waste_disposal=yes];
      {material_filters}
    );
    out center;
    """

    headers = {"User-Agent": "Eco-Mind/1.0 (contact@example.com)"}

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post(OVERPASS_API, data={"data": query}, headers=headers)
            r.raise_for_status()
            resp = r.json()
            elements = resp.get("elements", [])

            results = []
            for el in elements:
                tags = el.get("tags", {})
                name = tags.get("name") or "Unnamed Facility"

                # Get lat/lon
                if el.get("type") == "node":
                    lat, lon = el.get("lat"), el.get("lon")
                else:
                    center = el.get("center") or {}
                    lat, lon = center.get("lat"), center.get("lon")

                # Detect materials handled
                materials = [
                    label for key, label in {
                        "recycling:plastic": "Plastic",
                        "recycling:glass": "Glass",
                        "recycling:paper": "Paper",
                        "recycling:metal": "Metal",
                        "recycling:batteries": "Batteries",
                        "recycling:electric_appliances": "Electronics",
                    }.items() if tags.get(key) in ["yes", "true", "1"]
                ]
                description = ", ".join(materials) if materials else "General recycling or disposal"

                results.append({
                    "id": el.get("id"),
                    "name": name,
                    "description": description,
                    "lat": lat,
                    "lon": lon,
                    "tags": tags
                })

            return results
        except Exception as e:
            print(f"[overpass_recycling_near] Error: {e}")
            return []


# ----------------------------------------------------------------
# Earth911 — optional secondary dataset (requires API key)
# ----------------------------------------------------------------
async def earth911_locations(
        lat: float,
        lon: float,
        material_id: int = 56,
        radius_km: int = 50
) -> List[Dict]:
    """
    Search Earth911 (if an API key is available) for additional recycling centers.
    https://earth911.com/api/
    """
    if not settings.earth911_api_key:
        return []

    url = "https://api.earth911.com/earth911.searchLocations"
    params = {
        "api_key": settings.earth911_api_key,
        "latitude": lat,
        "longitude": lon,
        "material_id": material_id,
        "max_distance": radius_km,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        try:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json()
            locations = data.get("result", [])
            results = []

            for loc in locations:
                results.append({
                    "id": loc.get("location_id"),
                    "name": loc.get("description") or "Unnamed Facility",
                    "lat": loc.get("latitude"),
                    "lon": loc.get("longitude"),
                    "description": loc.get("description") or "Recycling center",
                    "materials": loc.get("materials"),
                    "address": loc.get("address1"),
                })
            return results

        except Exception as e:
            print(f"[earth911_locations] Error: {e}")
            return []
