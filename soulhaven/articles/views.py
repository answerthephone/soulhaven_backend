from django.shortcuts import render
from .models import Article


def latest_article_detail(request):
    """
    View that retrieves and displays the most recently published article.

    - Fetches the latest article based on the published date.
    - Passes it to the 'article_detail.html' template for rendering.

    Context:
    - article: The most recent Article instance.
    """
    latest_article = Article.objects.order_by('-published_date').first()
    context = {
        'article': latest_article
    }
    return render(request, 'article_detail.html', context)