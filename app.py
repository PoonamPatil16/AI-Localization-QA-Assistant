from flask import Flask, render_template, request
from flask import send_file
import io
import csv
from qa_engine import run_qa
from terminology import load_terminology

app = Flask(__name__)

def read_csv(file):
    data = []

    try:
        decoded_file = file.read().decode('utf-8-sig').splitlines()
    except UnicodeDecodeError:
        file.seek(0)
        decoded_file = file.read().decode('latin-1').splitlines()

    reader = csv.DictReader(decoded_file)

    for row in reader:
        clean_row = {
            "English": row.get("English", "").strip(),
            "Hindi": row.get("Hindi", "").strip()
        }
        data.append(clean_row)

    return data

def create_export_file(results):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["English", "Hindi", "Issues", "AI Suggestion"])

    for row in results:
        writer.writerow([
            row["English"],
            row["Hindi"],
            row["Issues"],
            row["Suggestion"]
        ])

    output.seek(0)
    return output

@app.route("/", methods=["GET", "POST"])
def index():
    results = None

    if request.method == "POST":
        file = request.files.get("file")

        if file:
            data = read_csv(file)
            results = run_qa(data)

    return render_template("index.html", results=results)

@app.route("/export", methods=["POST"])
def export():
    results = request.form.get("results")

    if results:
        import json
        results = json.loads(results)

        output = create_export_file(results)

        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype="text/csv",
            as_attachment=True,
            download_name="qa_report.csv"
        )


if __name__ == "__main__":
    load_terminology()
    from terminology import preferred_terms
    print("Loaded Terms:", preferred_terms)
    app.run(debug=True)