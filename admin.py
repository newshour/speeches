from django.contrib import admin
from speeches.models import Speech, FootnoteType, Footnote


class FootnoteInline(admin.StackedInline):
    model = Footnote
    extra = 3


class SpeechAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    inlines = [FootnoteInline]


class FootnoteTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(FootnoteType, FootnoteTypeAdmin)
admin.site.register(Speech, SpeechAdmin)