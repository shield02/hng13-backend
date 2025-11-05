from typing import Optional, List, Any, Tuple, Dict, Set
from ..services import recycle_lookup, chat_memory
from ..core.config import settings

# ------------------------------------------------------
# Context-aware Eco Tips
# ------------------------------------------------------
ECO_TIPS = {
    "plastic": [
        "No recycling facilities nearby, but here are some plastic reuse ideas:",
        "• Reuse bottles for watering plants or storage.",
        "• Use refill stations instead of single-use plastics.",
        "• Check if supermarkets accept plastic bag returns.",
    ],
    "battery": [
        "Couldn’t find local battery drop-off centers.",
        "• Store used batteries in a container until proper disposal is available.",
        "• Never throw them in the bin — they can leak chemicals.",
        "• Many electronics stores accept them for recycling.",
    ],
    "glass": [
        "No glass recycling centers nearby.",
        "• Reuse jars as storage containers.",
        "• Upcycle bottles into décor or planters.",
        "• Some bars or restaurants accept clean glass bottles.",
    ],
    "electronics": [
        "No e-waste centers nearby.",
        "• Donate or sell old electronics if working.",
        "• Ask phone stores or repair shops if they accept e-waste.",
        "• Avoid burning electronics — it releases toxins.",
    ],
    "default": [
        "No dedicated recycling or waste center was found nearby.",
        "Try these eco-friendly steps:",
        "• Reuse jars, bottles, or containers for storage.",
        "• Donate items instead of discarding them.",
        "• Compost organic waste to reduce landfill load.",
    ],
}


# ------------------------------------------------------
# Message Processing / Intent Detection
# ------------------------------------------------------
async def process_message(user_id: str, message: str, image_url: Optional[str] = None) -> str:
    """
    Handles general user input and detects intent (recycling, tips, help).
    Delegates recycling lookups to find_recycling_centers_by_city().
    """
    text = (message or "").lower()
    await chat_memory.append_message(user_id, "user", message or (image_url or "[image]"))

    if any(w in text for w in ["recycle", "dispose", "throw", "where", "bin", "center"]):
        reply = (
            "Sure — please tell me your city or town name "
            "so I can find nearby recycling or waste disposal centers."
        )
        await chat_memory.append_message(user_id, "assistant", reply)
        return reply

    if any(w in text for w in ["tip", "reuse", "upcycle", "sustain", "alternative"]):
        reply = (
            "Eco tip: switch to reusable containers and donate items you no longer need. "
            "Want me to show more sustainability tips?"
        )
        await chat_memory.append_message(user_id, "assistant", reply)
        return reply

    reply = (
        "Hi I'm Eco-Mind — your sustainability assistant\n"
        "You can ask me things like:\n"
        "• 'How do I recycle plastic bottles in Lagos?'\n"
        "• 'Where can I dispose of old batteries?'\n"
        "• 'Give me eco-friendly tips.'"
    )
    await chat_memory.append_message(user_id, "assistant", reply)
    return reply


# ------------------------------------------------------
# Find Recycling Centers by City
# ------------------------------------------------------
async def find_recycling_centers_by_city(user_id: str, city: str, material: Optional[str] = "waste") -> str:
    """
    Find nearby recycling/waste disposal facilities for a given city.
    Combines OSM (Overpass) data + Earth911 (if configured).
    """
    try:
        await chat_memory.append_message(user_id, "user", f"[find facilities for {city} ({material})]")

        # --- Geocode city ---
        geo = await recycle_lookup.nominatim_geocode(city)
        if not geo:
            reply = (
                f"Sorry, I couldn’t locate '{city}'. "
                "Please check the spelling or try another nearby city."
            )
            await chat_memory.append_message(user_id, "assistant", reply)
            return reply

        lat, lon = float(geo.get("lat")), float(geo.get("lon"))
        intro = f"Searching for {material} recycling centers near {city.title()}..."
        await chat_memory.append_message(user_id, "assistant", intro)

        # --- OSM Query ---
        osm_results = await recycle_lookup.overpass_recycling_near(lat, lon, radius_m=7000, material=material)

        # --- Earth911 Query (optional) ---
        earth_results = []
        if settings.earth911_api_key:
            earth_results = await recycle_lookup.earth911_locations(lat, lon, material_id=56, radius_km=50)

        # --- Merge & deduplicate ---
        all_results = merge_results(osm_results, earth_results)
        if all_results:
            lines = [f"✅ Found {len(all_results)} recycling facilit{'ies' if len(all_results) > 1 else 'y'} near {city.title()}:"]
            for r in all_results[:5]:
                name = r.get("name") or "Unnamed Facility"
                desc = r.get("description") or r.get("materials") or "General recycling"
                lines.append(f"• {name} — {desc}")
            reply = "\n".join(lines)
            await chat_memory.append_message(user_id, "assistant", reply)
            return reply

        # --- No results → show material-specific eco tips ---
        tips = ECO_TIPS.get(material.lower(), ECO_TIPS["default"])
        reply = "\n".join(tips)
        await chat_memory.append_message(user_id, "assistant", reply)
        return reply

    except Exception as e:
        fallback = (
            "Something went wrong while searching for facilities. "
            "Here are a few eco-friendly tips instead:\n" + "\n".join(ECO_TIPS["default"])
        )
        await chat_memory.append_message(user_id, "assistant", fallback)
        print(f"[ERROR] {e}")
        return fallback


# ------------------------------------------------------
# Helper: Merge OSM + Earth911 Results
# ------------------------------------------------------
def to_float(value: Any) -> float:
    """Convert a value safely to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def rounded(value: float, digits: int = 3) -> float:
    """Round a float safely without confusing type checkers."""
    # Explicitly multiply/divide instead of using round()
    factor = 10 ** digits
    return int(value * factor) / factor


def merge_results(osm: List[Dict[str, Any]], earth: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge and deduplicate results based on name and coordinates (type-checker safe)."""
    seen: Set[Tuple[str, float, float]] = set()
    merged: List[Dict[str, Any]] = []

    for r in osm + earth:
        name = str(r.get("name") or "Unknown")

        lat_val = to_float(r.get("lat"))
        lon_val = to_float(r.get("lon"))

        # ✅ Use custom rounding to avoid Pyright's overload confusion
        lat_rounded = rounded(lat_val, 3)
        lon_rounded = rounded(lon_val, 3)

        key = (name, lat_rounded, lon_rounded)
        if key not in seen:
            seen.add(key)
            merged.append(r)

    return merged