from flask import Flask, render_template, request, jsonify
import scraper
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        results = scraper.buscar_negocios(query)
        return jsonify({"query": json.dumps(results, indent=2)})  # Devolver la consulta en formato JSON

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
