# Baby Name Selector

A web-based application that allows users to filter and remove baby names stored in a Google Sheets document. The project consists of a Flask backend for handling API requests and a frontend interface for user interaction.

## Features

- Fetch baby names from a Google Sheet based on gender and starting letter.

- Remove selected names from the Google Sheet.

- Interactive and user-friendly frontend.

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Fetch API)

- **Backend:** Python, Flask

- **Database:** Google Sheets API (via gspread)

## Setup Instructions

### Prerequisites

1. Python 3 installed on your system.

2. A Google Cloud project with Google Sheets API enabled.

3. A Google Sheets document with at least two columns: _Name_ and _Gender_.

4. A _credentials.json_ file with Google Service Account credentials.

## Installation

1. Clone this repository:

```
git clone https://github.com/your-username/baby-name-selector.git
cd baby-name-selector
```

2. Install dependencies:
```
pip install flask gspread google-auth
```
3. Place your _credentials.json_ file in the root directory.

4. Update the _SHEET_NAME_ variable in _app.py_ to match your Google Sheet's name.

5. Run the Flask server:
```
python app.py
```
6. Open your browser and go to:
```
http://127.0.0.1:5000/
```

## API Endpoints

### Fetch Names

- **Endpoint:** _GET /get_names_

- **Query Parameters:**

  - _gender (string)_ - Required

  - _start_letter_ (string) - Required

- **Example Request:**
```
http://127.0.0.1:5000/get_names?gender=Male&start_letter=A
```
- **Response:**
```
{ "names": ["Alexander", "Andrew"] }
```
### Remove Name

- **Endpoint:** _POST /remove_name_
- **Request Body:**
```
{ "name": "Alexander" }
```
- **Response:**
```
{ "message": "'Alexander' has been removed" }
```
## Troubleshooting
- If you get a _Not Found_ error when filtering names, ensure your frontend is calling the correct endpoint _(/get_names)_.
- If the server doesn't start, check that _credentials.json_ is correctly configured.
- Ensure you have installed all required dependencies with _pip install -r requirements.txt_.

## License

This project is open-source under the MIT License.
