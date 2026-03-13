from django.contrib import admin

from .models import AnalysisRecord


@admin.register(AnalysisRecord)
class AnalysisRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "readability_score", "created_at")
    search_fields = ("input_text",)
    readonly_fields = ("created_at",)
