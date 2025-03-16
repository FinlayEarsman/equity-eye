from rest_framework import serializers

from .models import Article
from .models import Asset
from .models import StockPrice


class AssetSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Asset.objects.create(
            name=validated_data.get('name'),
            ticker=validated_data.get('ticker'),
            summary=validated_data.get('summary')
        )

    class Meta:
        model = Asset
        fields = (
            "id",
            "name",
            "ticker",
            "summary"
        )


class SimpleAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            "id",
            "name",
            "ticker"
        )


class ArticleSerializer(serializers.ModelSerializer):
    assets = serializers.SlugRelatedField(queryset=Asset.objects.all(),
                                          many=True, slug_field='name')

    def create(self, validated_data):
        assets = validated_data.pop('assets', [])

        article = Article.objects.create(**validated_data)
        for a in assets:
            article.assets.add(a)

        return article

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "author",
            "source",
            "body",
            "url",
            "published",
            "assets"
        )
        depth = 1


class SimpleArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "body",
            "published",
        )


class StockPriceSerializer(serializers.ModelSerializer):
    asset = serializers.SlugRelatedField(
        many=False,
        queryset=Asset.objects.all(),
        slug_field='ticker'
    )

    class Meta:
        model = StockPrice
        fields = (
            'time',
            'asset',
            'open',
            'close',
            'high',
            'low',
            'volume'
        )
