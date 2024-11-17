from flask import Flask, request, jsonify
import requests
from config import GOOGLE_API_KEY

app = Flask(__name__)

@app.route('/hotels', methods=['GET'])
def get_hotels():
    location = request.args.get('location')  # Expecting "latitude,longitude"
    radius = request.args.get('radius', 5000)  # Radius in meters, default to 5km

    if not location:
        return jsonify({"error": "Missing 'location' parameter"}), 400

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": GOOGLE_API_KEY,
        "location": location,
        "radius": radius,
        "type": "lodging",  # Specifies hotels and similar accommodations
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch hotels"}), response.status_code

    data = response.json()
    hotels = [
        {
            "name": hotel.get("name"),
            "address": hotel.get("vicinity"),
            "rating": hotel.get("rating", "N/A"),
            "user_ratings_total": hotel.get("user_ratings_total", 0),
            "latitude": hotel["geometry"]["location"].get("lat"),
            "longitude": hotel["geometry"]["location"].get("lng"),
        }
        for hotel in data.get("results", [])
    ]

    return jsonify({"hotels": hotels})

if __name__ == '__main__':
    app.run(debug=True)
