from django.contrib import admin
from .models import *


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "slug",
        "created_at",
    ]
    exclude = ("slug",)


admin.site.register(Blog, BlogAdmin)
