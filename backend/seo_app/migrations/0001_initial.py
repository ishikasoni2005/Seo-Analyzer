from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AnalysisRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("input_text", models.TextField()),
                ("readability_score", models.PositiveSmallIntegerField()),
                ("keywords", models.JSONField(default=list)),
                ("suggested_keywords", models.JSONField(default=list)),
                ("seo_suggestions", models.JSONField(default=list)),
                ("optimized_text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
