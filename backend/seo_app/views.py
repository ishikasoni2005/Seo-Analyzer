import logging

from django.db import DatabaseError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AnalysisRecord
from .serializers import AnalyzeRequestSerializer, AnalyzeResponseSerializer
from .services import (
    KeywordExtractorService,
    KeywordInsertionService,
    ReadabilityService,
)
from .utils import build_seo_suggestions

logger = logging.getLogger(__name__)


class AnalyzeAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        request_serializer = AnalyzeRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        text = request_serializer.validated_data["text"]

        keyword_service = KeywordExtractorService()
        insertion_service = KeywordInsertionService()

        keyword_result = keyword_service.analyze(text)
        readability_score = ReadabilityService.score(text)
        optimized_text = insertion_service.optimize_text(
            text,
            keyword_result["suggested_keywords"],
        )
        seo_suggestions = build_seo_suggestions(
            text,
            readability_score,
            keyword_result["keywords"],
            keyword_result["suggested_keywords"],
        )

        payload = {
            "keywords": keyword_result["keywords"],
            "readability_score": readability_score,
            "suggested_keywords": keyword_result["suggested_keywords"],
            "seo_suggestions": seo_suggestions,
            "optimized_text": optimized_text,
        }

        try:
            AnalysisRecord.objects.create(
                input_text=text,
                readability_score=readability_score,
                keywords=payload["keywords"],
                suggested_keywords=payload["suggested_keywords"],
                seo_suggestions=payload["seo_suggestions"],
                optimized_text=optimized_text,
            )
        except DatabaseError as exc:
            logger.warning("Analysis record could not be saved: %s", exc)

        response_serializer = AnalyzeResponseSerializer(data=payload)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
