from django.db import models
from users.models import User
from datetime import datetime


class Link(models.Model):
    link_id = models.BigIntegerField()
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
    expires_at = models.DateTimeField()
    redirects = models.IntegerField(default=0)

    class Meta:
        db_table = "dim_all_links"
        verbose_name = "link"
        verbose_name_plural = "links"

    def save(self, *args, **kwargs):
        if self.expires_at is None:
            self.expires_at = self.created_at.date() + datetime.timedelta(days=30)
        super(Link, self).save(*args, **kwargs)

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
