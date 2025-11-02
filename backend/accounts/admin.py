from django.contrib import admin
from .models import OrganiserProfile

@admin.register(OrganiserProfile)
class OrganiserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'user__email')
    actions = ('mark_verified', 'mark_unverified')

    @admin.action(description="Mark selected as verified")
    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Mark selected as unverified")
    def mark_unverified(self, request, queryset):
        queryset.update(is_verified=False)
