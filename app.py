from flask import Flask, request, jsonify, render_template
import gspread
import random
from google.oauth2.service_account import Credentials

app = Flask(__name__, template_folder="templates")

# Load Google Sheets API credentials securely
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("your_credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Sheet
SHEET_NAME = "acottonsock's Baby Names (Responses)"
sheet = client.open(SHEET_NAME).sheet1

@app.route("/get_names", methods=["GET"])
def get_names():
    gender = request.args.get("gender")
    start_letter = request.args.get("start_letter")  # optional

    if not gender:
        return jsonify({"error": "Missing gender parameter"}), 400

    all_entries = sheet.get_all_records()

    # Filter by gender
    filtered = [
        entry["Name"]
        for entry in all_entries
        if entry["Gender"].strip().lower() == gender.lower()
        and entry["Name"].strip()  # ensure name exists
        and (not start_letter or entry["Name"].strip().lower().startswith(start_letter.lower()))
    ]

    filtered_names = list(set(filtered))  # deduplicate
    random_name = random.choice(filtered_names) if filtered_names else None

    return jsonify({
        "names": filtered_names,
        "random_name": random_name
    })

""" @app.route("/remove_name", methods=["POST"])
def remove_name():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Missing name parameter"}), 400

    try:
        cell = sheet.find(name)
        if cell:
            sheet.delete_rows(cell.row)
            return jsonify({"message": f"'{name}' has been removed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Name not found"}), 404 """

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")