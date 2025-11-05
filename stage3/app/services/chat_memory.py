import json
from typing import Any
from ..core.config import settings
from ..main import get_redis


async def append_message(user_id: str, role: str, content: str) -> None:
    """
    Append a chat message for a given user.
    Stored as a JSON list in Redis (FIFO).
    """
    redis = get_redis()
    key = f"chat:{user_id}:messages"
    item = json.dumps({"role": role, "content": content})

    await redis.rpush(key, item)
    await redis.expire(key, settings.chat_ttl_seconds)


async def get_history(user_id: str) -> list[dict[str, Any]]:
    """
    Retrieve chat history for a user.
    """
    redis = get_redis()
    key = f"chat:{user_id}:messages"
    messages = await redis.lrange(key, 0, -1)
    return [json.loads(m) for m in messages]


async def clear_history(user_id: str) -> None:
    """
    Delete a user's chat history.
    """
    redis = get_redis()
    key = f"chat:{user_id}:messages"
    await redis.delete(key)
