from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

WINDOW_SIZE = 10
WINDOW = []

MOCK_DATA = {
    'p': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
    'f': [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
    'e': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    'r': [15, 22, 8, 11, 23, 4, 16, 42, 7, 19]
}

def fetch_numbers_from_server(numberid):
    return MOCK_DATA.get(numberid, [])

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    if numberid not in MOCK_DATA:
        return jsonify({"error": "Invalid number ID"}), 400

    numbers = fetch_numbers_from_server(numberid)

    global WINDOW
    previous_state = WINDOW.copy()

    for number in numbers:
        if number not in WINDOW:
            if len(WINDOW) >= WINDOW_SIZE:
                WINDOW.pop(0)
            WINDOW.append(number)

    current_state = WINDOW
    average = sum(current_state) / len(current_state) if current_state else 0

    response = {
        "numbers": numbers,
        "windowPrevState": previous_state,
        "windowCurrState": current_state,
        "average": average
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
