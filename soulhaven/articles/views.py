from django.http import JsonResponse
from .models import Article

def latest_article_api(request):
    """
    API view that returns the most recently published article in JSON format.

    Returns:
    - JSON object with article fields, or a message if no article exists.
    """
    article = Article.objects.order_by('-published_date').first()

    if not article:
        return JsonResponse({'message': 'No articles available'}, status=404)

    return JsonResponse({
        'title_header': article.title_header,
        'paragraph1': article.paragraph1,
        'header2': article.header2,
        'paragraph2': article.paragraph2,
        'header3': article.header3,
        'paragraph3': article.paragraph3,
        'themes': article.get_themes_list(),
        'footer_note': article.footer_note,
        'published_date': article.published_date.isoformat(),
    })
