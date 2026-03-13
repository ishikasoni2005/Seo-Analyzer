from rest_framework import serializers


class AnalyzeRequestSerializer(serializers.Serializer):
    text = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        max_length=25000,
    )


class KeywordMetricSerializer(serializers.Serializer):
    word = serializers.CharField()
    frequency = serializers.IntegerField(min_value=0)
    density = serializers.FloatField(min_value=0)


class AnalyzeResponseSerializer(serializers.Serializer):
    keywords = KeywordMetricSerializer(many=True)
    readability_score = serializers.IntegerField(min_value=0, max_value=100)
    suggested_keywords = serializers.ListField(child=serializers.CharField())
    seo_suggestions = serializers.ListField(child=serializers.CharField())
    optimized_text = serializers.CharField()
