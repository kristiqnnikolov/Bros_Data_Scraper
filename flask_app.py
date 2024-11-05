from flask import Flask, jsonify, request
import json

app = Flask(__name__)
print(" * Data available here: http://127.0.0.1:5000/air_conditioners")
# Load the scraped data from the JSON file with UTF-8 encoding
def load_data():
    with open('bros.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Define the API endpoint to get all air conditioners
@app.route('/air_conditioners', methods=['GET'])
def get_air_conditioners():
    data = load_data()
    return jsonify(data)

# Define the API endpoint to get an air conditioner by its ID
@app.route('/air_conditioners/<int:ac_id>', methods=['GET'])
def get_air_conditioner(ac_id):
    data = load_data()
    air_conditioner = next((item for item in data if item['id'] == ac_id), None)
    if air_conditioner:
        return jsonify(air_conditioner)
    else:
        return jsonify({"error": "Air conditioner not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
