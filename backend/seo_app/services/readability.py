import math

import textstat


class ReadabilityService:
    @staticmethod
    def score(text):
        if not text.strip():
            return 0

        raw_score = textstat.flesch_reading_ease(text)
        if math.isnan(raw_score):
            return 0

        return max(0, min(100, round(raw_score)))
