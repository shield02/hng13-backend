Core Flow

Telex.im sends messages (user text or image) → FastAPI /telex/webhook

FastAPI parses payload → stores message + context in Redis

Message → agent.py

Detect intent (“recycle”, “find center”, “sustainable tip”, etc.)

Query recycle_lookup.py (Earth911 + OSM)

Or return advice from eco_tips.py

Reply is sent back → Telex (via REST API)

writing the core agent logic (the intelligent part that handles recycling lookups + tips)?