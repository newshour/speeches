from django.contrib import admin
from speeches.models import Speech, Footnote


class FootnoteInline(admin.StackedInline):
    model = Footnote
    extra = 3


class SpeechAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    inlines = [FootnoteInline]


admin.site.register(Speech, SpeechAdmin)