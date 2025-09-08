from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import json, requests

app = FastAPI()

# โหลด embedding model (ถ้าจะใช้ similarity ภายหลัง)
model = SentenceTransformer("all-MiniLM-L6-v2")

# โหลด substitution dictionary
with open("substitution.json", "r") as f:
    substitution_dict = json.load(f)

# ฟังก์ชันดึงรายละเอียดเมนูจาก ThemealDB
def fetch_meal_detail(idMeal: str):
    try:
        res = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={idMeal}")
        data = res.json()
        if not data or not data.get("meals"):
            return None
        m = data["meals"][0]
        ingredients = []
        for i in range(1, 21):
            ing = m.get(f"strIngredient{i}")
            if ing and ing.strip() != "":
                ingredients.append(ing.lower())
        return {
            "id": m.get("idMeal", ""),
            "name": m.get("strMeal", ""),
            "category": m.get("strCategory", ""),
            "area": m.get("strArea", ""),
            "thumb": m.get("strMealThumb", ""),
            "ingredients": ", ".join(ingredients)
        }
    except Exception as e:
        print("Error fetch_meal_detail:", e)
        return None

@app.get("/")
def home():
    return {"msg": "Hello from Render + FastAPI!"}

@app.get("/ai-search")
def ai_search(ingredients: list[str] = Query(...), top_k: int = 10):
    # 1. Ingredient Substitution (Synonym Expansion)
    expanded = []
    for ing in ingredients:
        ing_lower = ing.lower()
        expanded.append(ing_lower)
        if ing_lower in substitution_dict:
            expanded.extend(substitution_dict[ing_lower])
    expanded = list(set(expanded))  # ลบ duplicate

    # 2. ดึงเมนูจาก ThemealDB (filter.php)
    results = []
    for ing in expanded:
        try:
            res = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ing}")
            data = res.json()
            if not data or not data.get("meals"):
                continue
            for m in data["meals"]:
                detail = fetch_meal_detail(m["idMeal"])
                if detail:
                    detail["score"] = 1.0  # ตอนนี้ fix score, ภายหลังค่อยใส่ logic similarity ได้
                    results.append(detail)
        except Exception as e:
            print(f"Error fetching meals for {ing}:", e)

    # 3. ลบเมนูซ้ำ (บางที shrimp/prawn จะได้เมนูเดียวกัน)
    unique_results = {meal["id"]: meal for meal in results}.values()

    # 4. คืนค่า top_k
    return {"ingredients_used": expanded, "results": list(unique_results)[:top_k]}
