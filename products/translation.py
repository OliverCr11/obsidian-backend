from modeltranslation.translator import register, TranslationOptions
from .models import Glove

@register(Glove)
class GloveTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'hero_title_over_the_product',
        'hero_marketing_description'
    )
