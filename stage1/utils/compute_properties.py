import hashlib


def compute_properties(value: str) -> dict:
    """Compute string properties.

    Args:
        value (str): The string to compute.

    Returns:
        dict: The computed properties.
    """
    cleaned = value.strip()
    hash_val = hashlib.sha256(cleaned.encode()).hexdigest()
    freq_map = {}
    for ch in cleaned:
        freq_map[ch] = freq_map.get(ch, 0) + 1

    return {
        "length": len(cleaned),
        "is_palindrome": cleaned.lower() == cleaned[::-1].lower(),
        "unique_characters": len(set(cleaned)),
        "word_count": len(cleaned.split()),
        "sha256_hash": hash_val,
        "character_frequency_map": freq_map,
    }
