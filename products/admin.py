from django.contrib import admin
from .models import Glove

@admin.register(Glove)
class GloveAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
