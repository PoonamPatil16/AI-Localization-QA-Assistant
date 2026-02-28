import re
from terminology import check_terminology
from ai_suggestions import get_ai_suggestion


def is_english_present(text):
    if text is None:
        return False
    return bool(re.search(r'[A-Za-z]', text))


def check_missing_translation(hindi):
    return hindi.strip() == ""


def check_copy_paste(english, hindi):
    return english.strip().lower() == hindi.strip().lower()


def check_spacing_issue(hindi):
    return "  " in hindi


def run_qa(data):
    results = []

    for row in data:
        eng = row.get("English", "").strip()
        hin = row.get("Hindi", "").strip()

        issues = []

        # Missing
        if check_missing_translation(hin):
            issues.append("Missing Translation")

        else:
            if is_english_present(hin):
                issues.append("Contains English Text")

            if check_copy_paste(eng, hin):
                issues.append("Same as Source")

            if check_spacing_issue(hin):
                issues.append("Extra Spacing")

            term_issues = check_terminology(eng, hin)
            issues.extend(term_issues)

        # If no issues
        if not issues:
            issues.append("OK")

        # 🔹 AI Suggestion (uses raw issues list)
        suggestion = get_ai_suggestion(eng, hin, issues)

        # 🔹 Convert issues to string only for display
        display_issues = ", ".join(issues)

        results.append({
            "English": eng,
            "Hindi": hin,
            "Issues": display_issues,
            "Suggestion": suggestion
        })

    return results