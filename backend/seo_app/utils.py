import re
from functools import lru_cache

import spacy
from django.conf import settings

WORD_PATTERN = re.compile(r"\b[a-zA-Z][a-zA-Z'-]*\b")
NON_WORD_PATTERN = re.compile(r"[^a-z0-9\s-]+")


def tokenize_words(text):
    return WORD_PATTERN.findall(text.lower())


def normalize_phrase(value):
    lowered = value.lower().replace("_", " ").strip()
    cleaned = NON_WORD_PATTERN.sub(" ", lowered)
    return re.sub(r"\s+", " ", cleaned).strip()


def deduplicate_preserve_order(items):
    seen = set()
    ordered_items = []
    for item in items:
        normalized = normalize_phrase(item)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered_items.append(item.strip())
    return ordered_items


def count_phrase_occurrences(text, phrase):
    normalized_text = f" {normalize_phrase(text)} "
    normalized_phrase = normalize_phrase(phrase)
    if not normalized_phrase:
        return 0
    pattern = rf"(?<![a-z0-9-]){re.escape(normalized_phrase)}(?![a-z0-9-])"
    return len(re.findall(pattern, normalized_text))


@lru_cache(maxsize=1)
def get_nlp():
    model_name = getattr(settings, "SPACY_MODEL", "en_core_web_sm")
    try:
        return spacy.load(model_name)
    except OSError:
        nlp = spacy.blank("en")
        if "sentencizer" not in nlp.pipe_names:
            nlp.add_pipe("sentencizer")
        return nlp


def get_stop_words():
    return get_nlp().Defaults.stop_words


def build_seo_suggestions(text, readability_score, keyword_metrics, suggested_keywords):
    suggestions = []
    word_count = len(tokenize_words(text))
    sentence_lengths = [
        len(tokenize_words(sentence))
        for sentence in re.split(r"[.!?]+", text)
        if sentence.strip()
    ]

    if readability_score < 60:
        suggestions.append(
            "Shorten long sentences and prefer everyday language to lift readability."
        )

    if sentence_lengths and max(sentence_lengths) > 28:
        suggestions.append(
            "Break the longest sentence into two smaller ideas to improve scanability."
        )

    if word_count < 150:
        suggestions.append(
            "Add supporting detail, examples, or FAQs so the page covers the topic more completely."
        )

    if keyword_metrics:
        highest_density = max(keyword_metrics, key=lambda item: item["density"])
        if highest_density["density"] > 4.5:
            suggestions.append(
                f"Reduce repetition of '{highest_density['word']}' to avoid keyword stuffing."
            )

        if not any(item["density"] >= 1.0 for item in keyword_metrics):
            suggestions.append(
                "Reinforce your primary keyword in headings and early body copy."
            )
    else:
        suggestions.append(
            "Introduce a clearer primary topic term so search engines can understand the page focus."
        )

    if suggested_keywords:
        joined_keywords = ", ".join(suggested_keywords[:3])
        suggestions.append(
            f"Work related terms like {joined_keywords} into headings or supporting paragraphs."
        )

    if not suggestions:
        suggestions.append(
            "The draft is balanced already; focus next on metadata, headings, and internal links."
        )

    return suggestions
