from flask import Flask, request, jsonify
from flask_cors import CORS

from scraper import scrape_amazon

app = Flask(__name__)

# ENABLE CORS
CORS(app)


@app.route("/scrape", methods=["POST"])
def scrape_product():

    data = request.json

    asin = data.get("asin")

    if not asin:

        return jsonify({
            "error": "ASIN is required"
        })

    product = scrape_amazon(asin)

    return jsonify(product)


@app.route("/")
def home():

    return "Amazon Scraper API Running"


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )