import requests, json, time
from typing import List, Dict

THEMEALDB_SEARCH = "https://www.themealdb.com/api/json/v1/1/search.php?s={q}"
CACHE_PATH = "meal_cache.json"

def _extract_ingredients(meal: Dict) -> list:
    ings = []
    for i in range(1, 21):
        v = (meal.get(f"strIngredient{i}") or "").strip()
        if v:
            ings.append(v)
    return ings

def fetch_meals_initial() -> List[Dict]:
    # ไล่ A-Z เพื่อกวาดสูตรจำนวนมากเข้ามาแคช
    all_meals = []
    for ch in "abcdefghijklmnopqrstuvwxyz":
        res = requests.get(THEMEALDB_SEARCH.format(q=ch), timeout=20)
        data = res.json()
        meals = data.get("meals") or []
        all_meals.extend(meals)
        time.sleep(0.2)
    # unique โดย idMeal
    uniq = {m["idMeal"]: m for m in all_meals}.values()
    # แนบ fields ที่ใช้จริง
    enriched = []
    for m in uniq:
        m["ingredients_list"] = _extract_ingredients(m)
        m["thumb"] = m.get("strMealThumb")
        enriched.append(m)
    return enriched

def ensure_cache(path: str = CACHE_PATH) -> List[Dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        meals = fetch_meals_initial()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meals, f, ensure_ascii=False, indent=2)
        return meals

def reload_cache(path: str = CACHE_PATH) -> int:
    meals = fetch_meals_initial()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meals, f, ensure_ascii=False, indent=2)
    return len(meals)
