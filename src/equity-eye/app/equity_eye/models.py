from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10, unique=True)
    summary = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=80, blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    body = models.TextField(max_length=15500, default='')
    imported = models.DateField(auto_now_add=True)
    published = models.DateField()
    url = models.URLField(unique=True)
    assets = models.ManyToManyField(Asset, related_name="articles", blank=True)

    class Meta:
        ordering = ('-imported',)

    def __str__(self):
        return self.title


class StockPrice(models.Model):
    time = models.DateTimeField(db_index=True)
    asset = models.ForeignKey(Asset, related_name="prices",
                              on_delete=models.CASCADE)
    open = models.DecimalField(max_digits=20, decimal_places=6)
    close = models.DecimalField(max_digits=20, decimal_places=6)
    high = models.DecimalField(max_digits=20, decimal_places=6)
    low = models.DecimalField(max_digits=20, decimal_places=6)
    volume = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['time', 'asset'],
                                    name='daily asset price')
        ]
