from django.shortcuts import render
from challenges.models import Challenge
from articles.models import Article
from experts.models import Expert
from appointment.forms import AppointmentForm

def homepage(request):
    """
    Renders the homepage with dynamic platform content.

    Features:
    - Displays all active challenges.
    - Shows the most recent article.
    - Lists all platform experts.
    - Includes an appointment form.

    POST Logic:
    - If the request is POST and the form is valid:
        - Saves the appointment.
        - Sets a success flag to trigger a success message or behavior on the frontend.
        - Resets the form to blank after successful submission.

    Context:
    - challenges: All currently active challenges.
    - latest_article: Most recently published article.
    - experts: All expert profiles.
    - form: AppointmentForm instance (empty or pre-filled on error).
    - success: Boolean indicating whether an appointment was successfully submitted.

    Returns:
    - Rendered 'main/homepage.html' template with context.
    """
    challenges = Challenge.objects.filter(active=True)
    latest_article = Article.objects.order_by('-published_date').first()
    experts = Expert.objects.all()
    form = AppointmentForm()
    success = False

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = AppointmentForm()

    return render(request, 'main/homepage.html', {
        'challenges': challenges,
        'latest_article': latest_article,
        'experts': experts,
        'form': form,
        'success': success,
    })
