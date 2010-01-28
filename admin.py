from django.contrib import admin
from speeches.models import Speech, FootnoteType, Footnote, GuestProfile, GuestProfileImage


class FootnoteInline(admin.StackedInline):
    model = Footnote
    extra = 3

class GuestProfileImageInline(admin.StackedInline):
    model = GuestProfileImage

class SpeechAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    inlines = [FootnoteInline]


class FootnoteTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GuestProfileAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail_view', 'get_full_name')
    list_display_links = ('admin_thumbnail_view', 'get_full_name')
    inlines = [GuestProfileImageInline]


class FootnoteAdmin(admin.ModelAdmin):
    list_display = ('created', 'author', 'note_type', 'index', 'public')
    list_filter = ('public', 'author', 'note_type', 'index')
    ordering = ('-created',)

admin.site.register(FootnoteType, FootnoteTypeAdmin)
admin.site.register(Speech, SpeechAdmin)
admin.site.register(GuestProfile, GuestProfileAdmin)
admin.site.register(Footnote, FootnoteAdmin)
