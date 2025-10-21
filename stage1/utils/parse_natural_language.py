def parse_natural_language(query: str):
    """Simple keyword-based query parser for demonstration."""
    q = query.lower()
    filters = {}

    if "palindromic" in q or "palindrome" in q:
        filters["is_palindrome"] = True
    if "single word" in q or "one word" in q:
        filters["word_count"] = 1
    if "longer than" in q:
        try:
            num = int(q.split("longer than")[1].split()[0])
            filters["min_length"] = num + 1
        except Exception:
            pass

    if "containing the letter" in q:
        letter = q.split("containing the letter")[-1].strip().split()[0]
        filters["contains_character"] = letter
    elif "containing the" in q:
        # fallback for "first vowel"
        if "first vowel" in q:
            filters["contains_character"] = "a"

    return filters
