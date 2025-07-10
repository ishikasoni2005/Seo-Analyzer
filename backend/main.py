from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Enable CORS (for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the SEO Analyzer API"}

# API key for TextRazor
TEXTRAZOR_API_KEY = "fc9aad9c33e4ad30de784f3f7b89300efa66e1653db5b60ffa7767ef"

# Input model
class TextInput(BaseModel):
    text: str

# Main SEO analyzer route
@app.post("/analyze")
async def analyze_text(data: TextInput):
    response = requests.post(
        "https://api.textrazor.com/",
        data={
            "text": data.text,
            "extractors": "entities,topics,words"
        },
        headers={
            "x-textrazor-key": TEXTRAZOR_API_KEY
        }
    )

    if response.status_code != 200:
        return {"error": "TextRazor API error", "status_code": response.status_code}

    result = response.json()
    response_data = result.get("response", {})

    # Extract keywords from topics
    keywords = [
        topic["label"]
        for topic in response_data.get("topics", [])
        if isinstance(topic.get("label"), str) and not any(char.isdigit() for char in topic["label"])
    ]

    # Fallback: extract from entities if topics are not available
    if not keywords:
        keywords = [
            entity["entityId"]
            for entity in response_data.get("entities", [])
            if isinstance(entity.get("entityId"), str) and not any(char.isdigit() for char in entity["entityId"])
        ]

    # Limit to top 5
    keywords = keywords[:5]

    # Readability and suggestions (static for now)
    readability_score = 70.2
    suggestions = [
        "Use active voice for clarity.",
        "Break long sentences for better readability.",
        "Include keywords in headings and subheadings."
    ]

    # Append keywords at end of text, separated
    if keywords:
        updated_text = data.text.strip() + " — Keywords: " + ", ".join(keywords)
    else:
        updated_text = data.text

    return {
        "readability": readability_score,
        "suggestions": suggestions,
        "keywords": keywords,
        "updated_text": updated_text
    }