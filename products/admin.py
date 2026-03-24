from django.contrib import admin
from .models import Glove, Category, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Glove)
class GloveAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'collection_type', 'price', 'stock', 'created_at')
    list_filter = ('category', 'collection_type', 'size')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
