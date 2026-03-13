from seo_app.utils import count_phrase_occurrences, get_nlp


class KeywordInsertionService:
    insertion_patterns = (
        "especially for {keyword}",
        "with a stronger focus on {keyword}",
        "while reinforcing {keyword}",
        "to support {keyword}",
    )

    def optimize_text(self, text, suggested_keywords):
        missing_keywords = [
            keyword
            for keyword in suggested_keywords
            if count_phrase_occurrences(text, keyword) == 0
        ][:3]

        if not missing_keywords:
            return text

        nlp = get_nlp()
        doc = nlp(text)
        sentences = [sentence.text.strip() for sentence in doc.sents if sentence.text.strip()]
        if not sentences:
            sentences = [text.strip()]

        for index, keyword in enumerate(missing_keywords):
            sentence_index = index % len(sentences)
            sentences[sentence_index] = self._blend_keyword(
                sentences[sentence_index],
                keyword,
                index,
            )

        return " ".join(sentences).strip()

    def _blend_keyword(self, sentence, keyword, pattern_index):
        trimmed = sentence.strip()
        if not trimmed:
            return f"Focus on {keyword}."

        has_terminal_punctuation = trimmed[-1] in ".!?"
        punctuation = trimmed[-1] if has_terminal_punctuation else "."
        body = trimmed[:-1].rstrip() if has_terminal_punctuation else trimmed
        insertion = self.insertion_patterns[pattern_index % len(self.insertion_patterns)]

        if len(body.split()) > 8:
            return f"{body}, {insertion.format(keyword=keyword)}{punctuation}"

        return f"{body} and {keyword}{punctuation}"
