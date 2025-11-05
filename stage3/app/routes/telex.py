import re
import asyncio

from fastapi import APIRouter, BackgroundTasks

from ..core import agent
from ..models.schemas import TelexIncoming, TelexResponse
from ..services import chat_memory, recycle_lookup

router = APIRouter()

@router.post("/webhook")
async def telex_webhook(payload: TelexIncoming, background_tasks: BackgroundTasks):
    """
    Handles conversational recycling queries:
    - Extract city and material (e.g., 'plastic', 'batteries')
    - Use Nominatim + Overpass to find nearby recycling facilities
    - Fall back to eco tips if none found
    """

    user_id = payload.user_id
    message = (payload.message or "").strip()

    if not message:
        reply = (
            "Hi there! I can help you find where to recycle things around you.\n"
            "Try asking something like:\n"
            "• 'Where can I recycle plastic bottles in Abuja?'\n"
            "• 'Battery recycling near Enugu'\n"
            "Please tell me your city to begin."
        )
        await chat_memory.append_message(user_id, "assistant", reply)
        return TelexResponse(user_id=user_id, response=reply)

    # Try to extract city name (simple heuristic: capitalized words or prepositions like "in <city>")
    city_match = re.search(r"\bin\s+([A-Z][a-zA-Z]+)", message)
    city = city_match.group(1) if city_match else None

    if not city:
        reply = (
            "I couldn't tell which city you're in. \n"
            "Please mention your city name, for example: 'I live in Lagos' or 'Recycle plastic in Abuja'."
        )
        await chat_memory.append_message(user_id, "assistant", reply)
        return TelexResponse(user_id=user_id, response=reply)

    # Geocode the city
    geo = await recycle_lookup.nominatim_geocode(city)
    if not geo:
        reply = f"Sorry, I couldn't locate '{city}'. Please check the spelling or try a nearby city."
        await chat_memory.append_message(user_id, "assistant", reply)
        return TelexResponse(user_id=user_id, response=reply)

    # Try to extract material type (optional)
    materials = ["plastic", "glass", "metal", "paper", "battery", "electronics"]
    found_material = next((m for m in materials if m in message.lower()), "waste")

    reply = f"Searching for {found_material} recycling facilities near {city}..."
    await chat_memory.append_message(user_id, "assistant", reply)

    # Run async search in the background
    background_tasks.add_task(lambda: asyncio.run(agent.find_recycling_centers_by_city(user_id, city, found_material)))

    return TelexResponse(user_id=user_id, response=reply)
