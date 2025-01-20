# api/index.py
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from flask_cors import CORS

CORS(app)

# Load the marks data
with open("marks.json", "r") as f:
    marks_data = json.load(f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get("name", [])

        # Fetch marks for the given names
        marks = [
            next((item["marks"] for item in marks_data if item["name"] == name), None)
            for name in names
        ]

        # Prepare the response
        response = {"marks": marks}
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))
