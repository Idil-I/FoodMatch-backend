# 🍽️ FoodMatch – AI-Powered Recipe Search Application

A mobile application that recommends recipes based on available ingredients using AI/NLP techniques.

## 🚀 Features
- Recommend recipes based on ingredients you have
- Ingredient substitution system (e.g. prawn = shrimp)
- User authentication via Supabase
- Real-time database management
- Clean and intuitive mobile UI

## 🛠️ Tech Stack
- **Frontend:** React Native, Expo
- **Backend:** FastAPI (Python)
- **Database & Auth:** Supabase
- **NLP Model:** Sentence Transformers (all-MiniLM-L6-v2)
- **Recipe API:** TheMealDB

## ⚙️ Installation

### Frontend
```bash
git clone https://github.com/Idil-I/FoodMatch
cd FoodMatch
npm install
npx expo start
```

### Backend
```bash
git clone https://github.com/Idil-I/FoodMatch-backend
cd FoodMatch-backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📖 Usage
1. Sign up / Log in with your account
2. Enter ingredients you have available
3. Browse recommended recipes
4. Select a recipe to view details

## 📁 Project Structure

### Frontend
```
FoodMatch/
├── assets/         # Images and static files
├── navigation/     # Navigation configuration
├── screens/        # App screens
├── styles/         # Styling files
├── App.js          # Entry point
├── supabase.js     # Supabase configuration
└── package.json
```

### Backend
```
FoodMatch-backend/
├── main.py             # FastAPI app & endpoints
├── ai.py               # AI/NLP logic
├── data_loader.py      # Data loading utilities
├── substitution.json   # Ingredient substitution dictionary
├── meal_cache.json     # Cached meal data
├── requirements.txt    # Python dependencies
└── render.yaml         # Render deployment config
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/ai-search?ingredients=egg,milk` | Search recipes by ingredients |

## 👥 Contributors
- [Idil-I](https://github.com/Idil-I)
