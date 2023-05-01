from django.contrib import admin
from links.models import Link, Redirect

admin.site.register([Link, Redirect])
