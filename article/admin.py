from django.contrib import admin
from .models import Download
# Register your models here.


class DownloadAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("id", "jsonData", "created_at")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("jsonData",)
    # добавляем возможность фильтрации по дате
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"


admin.site.register(Download, DownloadAdmin)