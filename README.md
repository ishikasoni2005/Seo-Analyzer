# 🔍 SEO Analyzer

An intelligent SEO Analyzer that evaluates content for keyword performance, readability, and optimization opportunities.

Combines **TextRazor, spaCy, and textstat** to extract keywords, measure density, score readability, suggest related terms, and generate an optimized text draft — served through a Django REST API with a React frontend.

> Upgraded from a FastAPI prototype into a scalable full-stack architecture.

---

## ✨ Features

- Keyword extraction via TextRazor with local NLP fallback
- Keyword frequency and density analysis for top detected terms
- Readability scoring using Flesch Reading Ease (`textstat`)
- Smart keyword insertion using spaCy sentence segmentation
- REST API with persisted `AnalysisRecord` model for history
- React interface for running analysis and reviewing results

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django, Django REST Framework, `django-cors-headers` |
| Frontend | React, Vite, Axios |
| NLP | spaCy (`en_core_web_sm`), `textstat` |
| External API | TextRazor |
| Storage | SQLite |

---

## 📂 Project Structure

```text
seo-analyzer/
├── backend/
│   ├── django_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── seo_app/
│   │   ├── migrations/
│   │   ├── services/
│   │   │   ├── keyword_extractor.py
│   │   │   ├── readability.py
│   │   │   └── keyword_inserter.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── utils.py
│   ├── .env.example
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/react_app/
    ├── src/
    │   ├── components/
    │   │   ├── TextInput.jsx
    │   │   ├── KeywordTable.jsx
    │   │   ├── ReadabilityCard.jsx
    │   │   └── Suggestions.jsx
    │   ├── pages/
    │   │   └── Analyzer.jsx
    │   ├── services/
    │   │   └── api.js
    │   ├── App.jsx
    │   └── main.jsx
    ├── .env.example
    ├── package.json
    └── vite.config.js
```

---

## 🔌 API Reference

### `POST /api/analyze/`

**Request:**
```json
{
  "text": "user input content"
}
```

**Response:**
```json
{
  "keywords": [
    { "word": "seo", "frequency": 5, "density": 3.1 }
  ],
  "readability_score": 65,
  "suggested_keywords": ["optimization", "ranking"],
  "seo_suggestions": [
    "Shorten long sentences and prefer everyday language to lift readability."
  ],
  "optimized_text": "text with suggested keyword placements"
}
```

### Service Layer

| File | Responsibility |
|------|---------------|
| `keyword_extractor.py` | TextRazor call with local fallback; frequency and density calculation |
| `readability.py` | Flesch Reading Ease score via `textstat` |
| `keyword_inserter.py` | spaCy sentence segmentation to insert missing keywords |
| `views.py` | Pipeline orchestration, input validation, response + record storage |

---

## ⚙️ Setup

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python -m spacy download en_core_web_sm
python manage.py runserver
```

Add your TextRazor key to `backend/.env`:
```env
TEXTRAZOR_API_KEY=your-textrazor-api-key
```

Runs at `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend/react_app
npm install
cp .env.example .env
npm run dev
```

Expects backend at `http://127.0.0.1:8000/api` by default. Runs at `http://127.0.0.1:5173`.

---

## 🧪 Example Usage

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "SEO content should be easy to read and use related keywords naturally."}'
```

**Axios:**
```javascript
import axios from 'axios';

const api = axios.create({ baseURL: 'http://127.0.0.1:8000/api' });
const { data } = await api.post('/analyze/', {
  text: 'SEO content should be easy to read and use related keywords naturally.'
});
```

---

## 📝 Notes

- CORS enabled via `django-cors-headers` for local Vite development
- TextRazor fallback ensures analysis still works without an API key
- `AnalysisRecord` model persists request history for future scaling
- DRF test included at `backend/seo_app/tests.py`
