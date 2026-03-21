from django.contrib import admin
from .models import Glove, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Glove)
class GloveAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'collection_type', 'price', 'stock', 'created_at')
    list_filter = ('category', 'collection_type', 'size')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
