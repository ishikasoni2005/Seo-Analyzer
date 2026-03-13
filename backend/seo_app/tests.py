from unittest.mock import patch

from rest_framework.test import APITestCase


class AnalyzeAPIViewTests(APITestCase):
    @patch("seo_app.views.ReadabilityService.score", return_value=72)
    @patch(
        "seo_app.views.KeywordInsertionService.optimize_text",
        return_value="Optimized SEO text.",
    )
    @patch(
        "seo_app.views.KeywordExtractorService.analyze",
        return_value={
            "keywords": [{"word": "seo", "frequency": 3, "density": 2.5}],
            "suggested_keywords": ["optimization", "ranking"],
        },
    )
    def test_analyze_endpoint_returns_expected_shape(
        self,
        keyword_mock,
        insertion_mock,
        readability_mock,
    ):
        response = self.client.post(
            "/api/analyze/",
            {"text": "SEO content with room for improvement."},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["keywords"][0]["word"], "seo")
        self.assertEqual(response.data["readability_score"], 72)
        self.assertEqual(response.data["suggested_keywords"], ["optimization", "ranking"])
        self.assertIn("optimized_text", response.data)
        self.assertIn("seo_suggestions", response.data)

        keyword_mock.assert_called_once()
        insertion_mock.assert_called_once()
        readability_mock.assert_called_once()
