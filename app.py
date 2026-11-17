from flask import Flask, jsonify, request, render_template
import requests
from database import init_db, add_favorite, remove_favorite, get_favorites

app = Flask(__name__)
BASE = "https://www.themealdb.com/api/json/v1/1"
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recipe/<meal_id>")
def recipe_page(meal_id):
    return render_template("recipe.html")


@app.route("/favorites")
def favorites_page():
    return render_template("favorites.html")


@app.route("/api/search")
def search():
    q = request.args.get("q", "")
    data = requests.get(f"{BASE}/search.php", params={"s": q}).json()
    return jsonify(data["meals"] or [])


@app.route("/api/recipe/<meal_id>")
def recipe(meal_id):
    data = requests.get(f"{BASE}/lookup.php", params={"i": meal_id}).json()
    if not data["meals"]:
        return jsonify({"error": "not found"}), 404
    m = data["meals"][0]
    ingredients = []
    for i in range(1, 21):
        name = (m.get(f"strIngredient{i}") or "").strip()
        measure = (m.get(f"strMeasure{i}") or "").strip()
        if name:
            ingredients.append(f"{measure} {name}".strip())
    return jsonify({
        "id": m["idMeal"],
        "name": m["strMeal"],
        "category": m["strCategory"],
        "area": m["strArea"],
        "image": m["strMealThumb"],
        "instructions": m["strInstructions"],
        "ingredients": ingredients,
    })


@app.route("/api/favorites", methods=["GET"])
def list_favorites():
    return jsonify(get_favorites())


@app.route("/api/favorites", methods=["POST"])
def save_favorite():
    d = request.get_json()
    add_favorite(d["id"], d["name"], d["image"], d["category"], d["area"])
    return jsonify({"ok": True})


@app.route("/api/favorites/<meal_id>", methods=["DELETE"])
def delete_favorite(meal_id):
    remove_favorite(meal_id)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
