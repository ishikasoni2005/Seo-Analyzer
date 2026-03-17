# SEO Analyzer Full-Stack App

An intelligent SEO Analyzer that evaluates content for keyword performance, readability, and optimization opportunities. The project started as a FastAPI app and has now been upgraded into a scalable full-stack architecture using Django REST Framework and React.
The application combines TextRazor, spaCy, and `textstat` to extract keywords, measure keyword density, calculate readability, suggest related search terms, and produce an optimized text draft.

## Features

- Keyword extraction powered by TextRazor with local fallback logic
- Keyword frequency and density analysis for the top detected terms
- Readability scoring using `textstat`
- Smart keyword insertion suggestions using spaCy sentence segmentation
- Modern React interface for running analysis and reviewing results
- REST API backend designed for modular growth and cleaner maintenance

## Tech Stack

- Backend: Django, Django REST Framework, `django-cors-headers`
- Frontend: React, Vite, Axios
- NLP: spaCy, `textstat`
- External API: TextRazor
- Storage: SQLite by default, with a persisted `AnalysisRecord` model for future scaling

## Project Structure

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
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── .env.example
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   └── react_app/
│       ├── src/
│       │   ├── components/
│       │   │   ├── TextInput.jsx
│       │   │   ├── KeywordTable.jsx
│       │   │   ├── ReadabilityCard.jsx
│       │   │   └── Suggestions.jsx
│       │   ├── pages/
│       │   │   └── Analyzer.jsx
│       │   ├── services/
│       │   │   └── api.js
│       │   ├── App.jsx
│       │   ├── main.jsx
│       │   └── styles.css
│       ├── .env.example
│       ├── index.html
│       ├── package.json
│       └── vite.config.js
└── README.md
```

## Backend Overview

### `POST /api/analyze/`

Request body:

```json
{
  "text": "user input content"
}
```

Response shape:

```json
{
  "keywords": [
    {
      "word": "seo",
      "frequency": 5,
      "density": 3.1
    }
  ],
  "readability_score": 65,
  "suggested_keywords": [
    "optimization",
    "ranking"
  ],
  "seo_suggestions": [
    "Shorten long sentences and prefer everyday language to lift readability."
  ],
  "optimized_text": "text with suggested keyword placements"
}
```

### Service Layer

- `keyword_extractor.py`: calls TextRazor when an API key is present, falls back to local candidate extraction, and calculates keyword frequency and density
- `readability.py`: computes a Flesch Reading Ease score using `textstat`
- `keyword_inserter.py`: uses spaCy sentence segmentation to weave missing keywords into the draft
- `views.py`: orchestrates the pipeline, validates input, returns the API response, and stores analysis records

## Frontend Overview

The React app includes:

- A text editor with sample content loading
- An Analyze button wired to the DRF API through Axios
- A keyword table with frequency and density
- A readability score card
- Suggested keyword chips and SEO recommendations
- An optimized text preview

## Setup Instructions

### 1. Backend setup

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

Update `backend/.env` with your real TextRazor key:

```env
TEXTRAZOR_API_KEY=your-textrazor-api-key
```

### 2. Frontend setup

```bash
cd frontend/react_app
npm install
cp .env.example .env
npm run dev
```

By default, the React app expects the backend API at `http://127.0.0.1:8000/api`.

## Example API Integration

### cURL request

```bash
curl -X POST http://127.0.0.1:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "SEO content should be easy to read, cover the topic fully, and use related keywords naturally."
  }'
```

### Axios request

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
});

const { data } = await api.post('/analyze/', {
  text: 'SEO content should be easy to read and use related keywords naturally.',
});

console.log(data);
```

## Notes

- CORS is enabled through `django-cors-headers` for local Vite development.
- If TextRazor is unavailable, the backend falls back to local keyword extraction so the app still returns useful analysis.
- The Django app includes a simple `AnalysisRecord` model so request history can be persisted and extended later.
- A lightweight DRF test is included in `backend/seo_app/tests.py`.
