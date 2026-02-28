from terminology import preferred_terms

def get_ai_suggestion(english, hindi, issues):

    # Suggest if translation missing
    if "Missing Translation" in issues:
        return preferred_terms.get(english, "")

    # Suggest if terminology mismatch
    for issue in issues:
        if "Use preferred term" in issue:
            return preferred_terms.get(english, "")

    # Suggest if English present
    if "Contains English Text" in issues:
        return preferred_terms.get(english, "")

    return ""