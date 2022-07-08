from django.contrib import admin
from .models import Settings
from django import forms
from django.shortcuts import render
from django.urls import path


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['days'].help_text = 'Array of days to get the data points upto'

    class Meta:
        model = Settings
        fields = '__all__'

class SettingsFormAdmin(admin.ModelAdmin):
    form = SettingsForm


class SettingsAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('add-settings/', self.set_settings),]
        return new_urls + urls

    def set_settings(self, request):
        return render(request=request, template_name='admin/settings/settings/custom_settings_page.html')


admin.site.register(Settings, SettingsAdmin)