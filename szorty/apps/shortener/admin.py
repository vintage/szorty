from django.contrib import admin
from . import models


class WordAdmin(admin.ModelAdmin):
    pass


class ShortcutAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Word, WordAdmin)
admin.site.register(models.Shortcut, ShortcutAdmin)