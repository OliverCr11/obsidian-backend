from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    glove = models.ForeignKey('Glove', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(glove=self.glove).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.glove.name} (Primary: {self.is_primary})"
class Glove(models.Model):
    COLLECTION_CHOICES = [
        ('DROP', 'Limited Edition'),
        ('CORE', 'Standard Item'),
    ]

    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    category = models.ForeignKey(Category, related_name='gloves', on_delete=models.SET_NULL, null=True, blank=True)
    collection_type = models.CharField(max_length=4, choices=COLLECTION_CHOICES, default='DROP')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default='M')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
