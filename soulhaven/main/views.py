from django.http import JsonResponse
from challenges.models import Challenge
from articles.models import Article
from experts.models import Expert

def homepage_data_api(request):
    """
    Returns homepage data as JSON:
    - Active challenges
    - Latest article
    - List of experts

    This is used by the frontend to populate the dynamic content.
    """
    challenges = Challenge.objects.filter(active=True).values('id', 'name', 'description', 'star_reward')
    article = Article.objects.order_by('-published_date').first()
    experts = Expert.objects.all().values('id', 'name', 'specialization', 'experience')

    article_data = {
        'title_header': article.title_header,
        'paragraph1': article.paragraph1,
        'header2': article.header2,
        'paragraph2': article.paragraph2,
        'header3': article.header3,
        'paragraph3': article.paragraph3,
        'themes': article.get_themes_list(),
        'footer_note': article.footer_note,
        'published_date': article.published_date.isoformat(),
    } if article else None

    return JsonResponse({
        'challenges': list(challenges),
        'latest_article': article_data,
        'experts': list(experts),
    })
