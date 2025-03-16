from django.shortcuts import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

import urllib.parse
from datetime import date

from .models import Article
from .models import Asset
from .models import StockPrice
from .serializers import ArticleSerializer
from .serializers import SimpleArticleSerializer
from .serializers import AssetSerializer
from .serializers import SimpleAssetSerializer
from .serializers import StockPriceSerializer


def index(request):
    return HttpResponse(
        'Dashboard can be accessed at equity-eye.ida.gla.ac.uk')


# API Views for Article model
class ArticleView(APIView):
    def get(self, request, url=None, id=None, range=None):
        # returns if an article is in the database or not
        if url:
            decoded = urllib.parse.unquote(str(url))
            try:
                Article.objects.get(url=decoded)
            except Article.DoesNotExist:
                return Response({'not-exists': 'This article does not exist.'},
                                status=200)

            return Response({'exists': 'This article exists.'}, status=200)

        # returns data of a specific article
        elif id:
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                return Response({'not-exists': 'This article does not exist.'},
                                status=200)

            serialiser = ArticleSerializer(article)
            return Response({'article': serialiser.data}, status=200)

        # returns all articles associated with an asset within a window
        elif range:
            split_range = range.split('-')
            ticker = split_range[2]
            if split_range[0] == '0' or split_range[1] == '0':
                articles = Article.objects.filter(assets__ticker=ticker) \
                               .order_by('-published')[:18]
            else:
                min = date.fromtimestamp(int(split_range[0]))
                max = date.fromtimestamp(int(split_range[1]))
                articles = Article.objects.filter(assets__ticker=ticker) \
                    .filter(published__range=[min, max]) \
                    .order_by('published')
            serialiser = ArticleSerializer(articles, many=True)
            return Response({'articles': serialiser.data}, status=200)
        # returns bad request
        else:
            return Response(
                {'invalid-request': 'Provide either an id, range or url.'},
                status=400
            )

    # processes new articles sent from backend service
    def post(self, request):
        data = request.data
        articles = data['articles']

        for a in articles:
            new_article = ArticleSerializer(data=a)
            if new_article.is_valid():
                new_article.save()
            else:
                print(new_article.errors)

        return Response({'status': 201, 'message': 'success'})


# API Views for Asset model
class AssetView(APIView):
    def get(self, request, ticker=None):
        # returns a specific asset's data
        if ticker:
            try:
                asset = Asset.objects.get(Q(ticker=ticker) | Q(name=ticker))
            except Asset.DoesNotExist:
                return Response({'not-exists': 'This asset does not exist.'},
                                status=200)
            serialiser = AssetSerializer(asset)
            return Response({'asset': serialiser.data}, status=200)

        # returns all assets
        else:
            assets = Asset.objects.all().values('id', 'name', 'ticker')
            serialiser = SimpleAssetSerializer(assets, many=True)
            return Response({'assets': serialiser.data})

    # processes new assets sent from backend service
    def post(self, request):
        data = request.data
        assets = data['assets']

        for a in assets:
            new_asset = AssetSerializer(data=a)
            if new_asset.is_valid():
                new_asset.save()
            else:
                print(new_asset.errors)

        return Response({'status': 201, 'message': 'success'})


# API Views for StockPrice model
class StockPriceView(APIView):
    def get(self, request, id=None):
        if id:
            # returns all price data for a specific asset
            if id != "latest":
                try:
                    aggregates = StockPrice.objects.filter(asset__ticker=id)
                except StockPrice.DoesNotExist:
                    return Response({'not-exists':
                                    'This asset does not exist.'},
                                    status=200)

                serialiser = StockPriceSerializer(aggregates, many=True)
                return Response({'aggregates': serialiser.data}, status=200)
            # returns the timestamp of the most recent of price data collected
            else:
                try:
                    newest_aggregate_time = StockPrice.objects.latest(
                        'time').time
                except StockPrice.DoesNotExist:
                    return Response({'not-exists': 'No assets in database'},
                                    status=200)

                return Response({'latest': newest_aggregate_time}, status=200)
        # bad request
        else:
            return Response({'not-exists': 'This asset does not exist.'},
                            status=200)

    # processes new set of price data from backend service
    def post(self, request):
        data = request.data
        all_aggregates = data['asset_aggregates']

        for asset_aggregates in all_aggregates:
            ticker = asset_aggregates['ticker']
            aggregates = asset_aggregates['aggregates']
            for a in aggregates:
                a['asset'] = ticker
                new_aggregate = StockPriceSerializer(data=a)
                if new_aggregate.is_valid():
                    new_aggregate.save()
                else:
                    print(new_aggregate.errors)

        return Response({'status': 201, 'message': 'success'})


# API view for the search functionality
# returns result of query
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    page = request.data.get('page', '')

    if query:
        articles = Article.objects.filter(Q(assets__name__icontains=query)) \
            .values('id', 'title', 'body', 'published') \
            .order_by('-published')
        paginator = Paginator(articles, 25)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            articles = paginator.page(paginator.num_pages)

        assets = Asset.objects.filter(name=query)
        article_serialiser = SimpleArticleSerializer(articles, many=True)
        asset_serialiser = AssetSerializer(assets, many=True)
        return Response({
            "articles": article_serialiser.data,
            "assets": asset_serialiser.data
        })
    else:
        return Response({"articles": [], "assets": []})
