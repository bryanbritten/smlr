# Generated by Django 4.2 on 2023-05-01 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Link",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_id", models.CharField(max_length=15)),
                ("original", models.URLField()),
                ("shortened", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("expires_at", models.DateTimeField()),
                ("redirects", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "link",
                "verbose_name_plural": "links",
                "db_table": "dim_all_links",
            },
        ),
        migrations.CreateModel(
            name="Redirect",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("referer", models.URLField()),
                ("ip_address", models.CharField(max_length=15)),
                ("user_agent", models.TextField()),
                ("event_time", models.DateTimeField(auto_now_add=True)),
                (
                    "link_id",
                    models.ForeignKey(
                        db_column="link_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="links.link",
                    ),
                ),
            ],
            options={
                "verbose_name": "redirect",
                "verbose_name_plural": "redirects",
                "db_table": "fct_redirects",
            },
        ),
    ]