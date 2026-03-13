from django.db import models


class AnalysisRecord(models.Model):
    input_text = models.TextField()
    readability_score = models.PositiveSmallIntegerField()
    keywords = models.JSONField(default=list)
    suggested_keywords = models.JSONField(default=list)
    seo_suggestions = models.JSONField(default=list)
    optimized_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Analysis {self.pk} ({self.created_at:%Y-%m-%d %H:%M:%S})"
