from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from .models import Event, EventBeneficiary

class BeneficiaryInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Determine whether the parent form is being set to published
        # On the add/change form, the POST includes 'published' when checked.
        parent_published = False
        try:
            val = self.data.get('published', '')
            parent_published = str(val).lower() in ('on', 'true', '1')
        except Exception:
            parent_published = False

        if parent_published:
            total = 0
            for form in self.forms:
                if not hasattr(form, 'cleaned_data'):
                    continue
                if form.cleaned_data.get('DELETE', False):
                    continue
                alloc = form.cleaned_data.get('allocation_percent') or 0
                total += alloc

            if total != 100:
                raise forms.ValidationError(
                    "Beneficiary allocations must total exactly 100% when publishing."
                )

class EventBeneficiaryInline(admin.TabularInline):
    model = EventBeneficiary
    extra = 0
    formset = BeneficiaryInlineFormSet

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organiser', 'start_datetime', 'published')
    list_filter = ('published', 'start_datetime')
    search_fields = ('title', 'organiser__username')
    inlines = [EventBeneficiaryInline]

@admin.register(EventBeneficiary)
class EventBeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('event', 'charity', 'allocation_percent')
    list_filter = ('charity',)
    search_fields = ('event__title', 'charity__name')
