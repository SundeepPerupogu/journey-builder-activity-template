from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import pytz
import os

app = Flask(__name__)

def get_time_difference(future_date_str, user_timezone_str):
    try:
        # Parse the future date string
        future_date = datetime.strptime(future_date_str, "%Y-%m-%d %H:%M:%S")
        
        # Get the user's timezone
        user_timezone = pytz.timezone(user_timezone_str)
        
        # Localize the future date to the user's timezone
        future_date_localized = user_timezone.localize(future_date)
        
        # Get the current time in the user's timezone
        current_time = datetime.now(user_timezone)
        
        # Calculate the difference
        time_difference = future_date_localized - current_time
        
        return time_difference
    except Exception as e:
        return str(e)

@app.route('/time_difference', methods=['POST'])
def time_difference():
    data = request.json
    future_date_str = data.get('future_date')
    user_timezone_str = data.get('user_timezone')
    
    if not future_date_str or not user_timezone_str:
        return jsonify({"error": "Invalid input"}), 400

    time_difference = get_time_difference(future_date_str, user_timezone_str)
    if isinstance(time_difference, str):
        return jsonify({"error": time_difference}), 400

    return jsonify({"time_difference": str(time_difference)})

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
