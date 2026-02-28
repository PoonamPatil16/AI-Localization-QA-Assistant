import csv
import os

preferred_terms = {}

def load_terminology():
    global preferred_terms

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "terminology.csv")

    try:
        with open(file_path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                preferred_terms[row["English"].strip()] = row["Hindi"].strip()
    except Exception as e:
        print("Terminology load error:", e)
        preferred_terms = {}

def check_terminology(english, hindi):
    suggestions = []

    if english in preferred_terms:
        preferred = preferred_terms[english]

        if hindi.strip() != "" and hindi != preferred:
            suggestions.append(f"Use preferred term: {preferred}")

    return suggestions