import logging
from collections import Counter

import requests
from django.conf import settings

from seo_app.utils import (
    count_phrase_occurrences,
    deduplicate_preserve_order,
    get_nlp,
    get_stop_words,
    normalize_phrase,
    tokenize_words,
)

logger = logging.getLogger(__name__)

RELATED_KEYWORD_MAP = {
    "seo": ["optimization", "ranking", "organic traffic", "search intent"],
    "content": ["content strategy", "audience intent", "topic authority"],
    "keyword": ["search volume", "semantic keyword", "SERP visibility"],
    "marketing": ["conversion rate", "brand visibility", "campaign performance"],
    "readability": ["content clarity", "user engagement", "reading ease"],
}


class KeywordExtractorService:
    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key if api_key is not None else settings.TEXTRAZOR_API_KEY
        self.api_url = (
            api_url if api_url is not None else settings.TEXTRAZOR_API_URL
        )

    def analyze(self, text):
        total_words = max(len(tokenize_words(text)), 1)
        textrazor_candidates = self._fetch_textrazor_candidates(text)
        local_candidates = self._extract_local_candidates(text)
        combined_candidates = deduplicate_preserve_order(
            textrazor_candidates + local_candidates
        )

        keywords = self._build_keyword_metrics(text, total_words, combined_candidates)
        suggested_keywords = self._build_suggested_keywords(
            text, combined_candidates, keywords
        )

        return {
            "keywords": keywords[: settings.KEYWORD_LIMIT],
            "suggested_keywords": suggested_keywords[
                : settings.SUGGESTED_KEYWORD_LIMIT
            ],
        }

    def _fetch_textrazor_candidates(self, text):
        if not self.api_key:
            return []

        try:
            response = requests.post(
                self.api_url,
                data={
                    "text": text,
                    "extractors": "entities,topics,words",
                },
                headers={"x-textrazor-key": self.api_key},
                timeout=15,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.warning("TextRazor request failed: %s", exc)
            return []

        try:
            payload = response.json().get("response", {})
        except ValueError as exc:
            logger.warning("TextRazor returned invalid JSON: %s", exc)
            return []

        topics = sorted(
            payload.get("topics", []),
            key=lambda item: item.get("score", 0),
            reverse=True,
        )
        entities = sorted(
            payload.get("entities", []),
            key=lambda item: item.get("relevanceScore", 0),
            reverse=True,
        )
        words = payload.get("words", [])

        candidates = []
        for topic in topics:
            label = topic.get("label")
            if self._is_candidate(label):
                candidates.append(label)

        for entity in entities:
            label = entity.get("matchedText") or entity.get("entityId")
            if self._is_candidate(label):
                candidates.append(label)

        for word in words:
            token = word.get("lemma") or word.get("token")
            if self._is_candidate(token):
                candidates.append(token)

        return deduplicate_preserve_order(candidates)

    def _extract_local_candidates(self, text):
        nlp = get_nlp()
        doc = nlp(text)
        stop_words = get_stop_words()

        if doc.has_annotation("POS"):
            candidate_terms = [
                (token.lemma_ or token.text).lower()
                for token in doc
                if token.pos_ in {"NOUN", "PROPN", "ADJ"}
                and token.is_alpha
                and len(token.text) > 2
                and token.text.lower() not in stop_words
            ]
        else:
            candidate_terms = [
                token
                for token in tokenize_words(text)
                if token not in stop_words and len(token) > 2
            ]

        ranked = Counter(candidate_terms).most_common(settings.KEYWORD_LIMIT * 3)
        return [term for term, _count in ranked]

    def _build_keyword_metrics(self, text, total_words, candidates):
        metrics = []
        for candidate in candidates:
            frequency = count_phrase_occurrences(text, candidate)
            if frequency < 1:
                continue

            normalized = normalize_phrase(candidate)
            word_length = max(len(normalized.split()), 1)
            metrics.append(
                {
                    "word": candidate.strip(),
                    "frequency": frequency,
                    "density": round((frequency * word_length / total_words) * 100, 2),
                }
            )

        metrics.sort(
            key=lambda item: (-item["frequency"], -item["density"], item["word"].lower())
        )
        return metrics

    def _build_suggested_keywords(self, text, candidates, keywords):
        existing_keywords = {
            normalize_phrase(keyword["word"])
            for keyword in keywords[: settings.KEYWORD_LIMIT]
        }
        suggestions = []

        for candidate in candidates:
            normalized = normalize_phrase(candidate)
            if not normalized or normalized in existing_keywords:
                continue
            if count_phrase_occurrences(text, candidate) == 0:
                suggestions.append(candidate.strip())

        for keyword in existing_keywords:
            suggestions.extend(RELATED_KEYWORD_MAP.get(keyword, []))

        if not suggestions:
            suggestions.extend(local for local in RELATED_KEYWORD_MAP.get("seo", []))

        return deduplicate_preserve_order(suggestions)

    @staticmethod
    def _is_candidate(value):
        normalized = normalize_phrase(value or "")
        return bool(normalized) and not any(char.isdigit() for char in normalized)
