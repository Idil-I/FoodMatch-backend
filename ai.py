from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_corpus(user_ingredients: List[str], recipes: List[Dict[str, str]]):
    user_text = ", ".join([i.strip().lower() for i in user_ingredients if i])
    rec_texts = [
        (r.get("idMeal"), r.get("strMeal"),
         ", ".join([x.strip().lower() for x in r.get("ingredients_list", [])]))
        for r in recipes
    ]
    corpus = [user_text] + [t[2] for t in rec_texts]
    return user_text, rec_texts, corpus

def recommend_recipes(user_ingredients: List[str],
                      recipes: List[Dict[str, str]],
                      top_k: int = 20):
    if not recipes:
        return []
    _, rec_texts, corpus = build_corpus(user_ingredients, recipes)

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    scored = []
    for (meal_id, meal_name, _), s in zip(rec_texts, sims):
        scored.append({"id": meal_id, "name": meal_name, "score": float(s)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]