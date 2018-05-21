import random

from apps.main.models import ScrapContent
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def MainView(request):
    articles = list(ScrapContent.objects.all())
    random.shuffle(articles)
    return render(request, 'main/main.html', {'articles': articles})
