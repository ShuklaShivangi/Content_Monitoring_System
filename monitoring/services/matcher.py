def calculate_score(keyword, content):
    keyword_lower = keyword.lower()
    title_lower = content.title.lower()
    body_lower = content.body.lower()

    # Exact match in title
    if keyword_lower == title_lower:
        return 100

    # Partial match in title
    if keyword_lower in title_lower:
        return 70

    # Match in body only
    if keyword_lower in body_lower:
        return 40

    return 0