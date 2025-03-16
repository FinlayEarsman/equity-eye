from django.contrib import admin
from .models import Article
from .models import Asset
from .models import StockPrice

# Register your models here.
admin.site.register(Article)
admin.site.register(Asset)
admin.site.register(StockPrice)


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
