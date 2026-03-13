# 🚀 SEO Analyzer Web App

An intelligent **SEO Analyzer** that evaluates textual content to improve **search engine visibility, readability, and keyword optimization**.

The application extracts important keywords, calculates keyword density, evaluates readability, and suggests keyword insertions for better SEO performance.

Originally built with **FastAPI**, the project has been upgraded to a **full-stack architecture using Django REST Framework and React** for better scalability, maintainability, and modern UI development.

The system integrates **TextRazor NLP API** and **spaCy** for advanced natural language processing and SEO insights.

---

# 📌 Features

### 🔍 Keyword Extraction
- Extracts top keywords from content using **TextRazor NLP API**
- Displays **keyword frequency and density**

### 📊 Readability Analysis
- Calculates readability scores for content quality evaluation
- Can integrate **textstat** for detailed readability metrics

### 🧠 Smart Keyword Suggestions
- Suggests missing keywords for better SEO performance
- Uses **spaCy NLP pipeline** to insert keywords naturally

### ✨ Content Optimization
- Generates an **optimized version of the input text**
- Improves keyword distribution and readability

### 🎨 Modern Web Interface
- Built with **React**
- Clean and responsive UI for real-time analysis

### 🔗 API-Based Architecture
- Backend powered by **Django REST Framework**
- Frontend communicates via REST APIs

---

# 🛠️ Tech Stack

| Layer | Technologies |
|------|--------------|
| **Frontend** | React, JavaScript, Axios |
| **Backend** | Django, Django REST Framework |
| **NLP Processing** | spaCy (`en_core_web_sm`) |
| **External API** | TextRazor NLP API |
| **Styling** | CSS3 / Responsive Design |
| **Development Tools** | Node.js, Python |

---

# 🧠 System Architecture




User Input (React UI)
│
▼
React Frontend
│
▼
Django REST API
│
├── TextRazor API → Keyword Extraction
│
├── spaCy NLP → Keyword Suggestions
│
└── Readability Analyzer
│
▼
SEO Analysis Results
│
▼
React Dashboard





---

# 📂 Project Structure



seo-analyzer/
│
├── backend/
│ ├── django_project/
│ │
│ ├── seo_app/
│ │ ├── services/
│ │ │ ├── keyword_extractor.py
│ │ │ ├── readability.py
│ │ │ └── keyword_inserter.py
│ │ │
│ │ ├── serializers.py
│ │ ├── views.py
│ │ ├── urls.py
│ │ └── models.py
│ │
│ ├── requirements.txt
│ └── manage.py
│
├── frontend/
│ ├── react_app/
│ │ ├── src/
│ │ │ ├── components/
│ │ │ │ ├── TextInput.jsx
│ │ │ │ ├── KeywordTable.jsx
│ │ │ │ ├── ReadabilityCard.jsx
│ │ │ │ └── Suggestions.jsx
│ │ │ │
│ │ │ ├── pages/
│ │ │ │ └── Analyzer.jsx
│ │ │ │
│ │ │ ├── services/
│ │ │ │ └── api.js
│ │ │ │
│ │ │ ├── App.jsx
│ │ │ └── main.jsx
│ │ │
│ │ └── package.json
│
└── README.md



---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/seo-analyzer.git
cd seo-analyzer



🖥️ Backend Setup (Django)
Create Virtual Environment
python -m venv venv
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Install spaCy Model
python -m spacy download en_core_web_sm
Run Django Server
python manage.py runserver
Backend will run at:
http://127.0.0.1:8000
🌐 Frontend Setup (React)
Navigate to frontend folder:
cd frontend/react_app
Install dependencies:
npm install
Run development server:
npm run dev
Frontend will run at:
http://localhost:5173
📊 Example API Request
Endpoint
POST /api/analyze/
Request Body
{
  "text": "SEO improves website visibility in search engines."
}
Response
{
  "keywords": [
    {
      "word": "SEO",
      "frequency": 2,
      "density": 3.2
    }
  ],
  "readability_score": 70,
  "suggested_keywords": ["optimization", "ranking"],
  "optimized_text": "SEO optimization improves website ranking in search engines."
}
🎯 Use Cases
Blog content optimization
SEO content strategy
Marketing content evaluation
Keyword density analysis
NLP-based content improvement
🔮 Future Improvements
AI-based SEO recommendations
SEO scoring system
Keyword ranking prediction
Chrome extension for live SEO analysis
Real-time collaborative editing
👩‍💻 Author
Ishika
Computer Science Student
Backend Developer | AI/ML Enthusiast
Focused on building scalable backend systems, NLP tools, and AI-powered developer applications.
