from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Glove, Category, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Glove)
class GloveAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'category', 'collection_type', 'price', 'stock', 'is_hero_drop', 'created_at')
    list_editable = ('is_hero_drop',)
    list_filter = ('category', 'collection_type', 'size', 'is_hero_drop')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
