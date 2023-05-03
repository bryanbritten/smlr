from django.db import models
from users.models import User
from datetime import datetime, timezone, timedelta


def calculate_expiration_date():
    dt = datetime.now() + timedelta(days=30)
    return dt.astimezone(tz=timezone.utc)


class Link(models.Model):
    link_id = models.TextField()
    original = models.URLField()
    shortened = models.URLField()
    created_by = models.ForeignKey(
        User,
        db_column="created_by",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=calculate_expiration_date)

    class Meta:
        db_table = "dim_all_links"
        verbose_name = "link"
        verbose_name_plural = "links"

    def __str__(self):
        return f"{self.shortened}"


class Redirect(models.Model):
    link_id = models.ForeignKey(
        Link,
        db_column="link_id",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    referer = models.URLField()
    ip_address = models.CharField(max_length=15)
    user_agent = models.TextField()
    event_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "fct_redirects"
        verbose_name = "redirect"
        verbose_name_plural = "redirects"
