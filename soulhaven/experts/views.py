from django.shortcuts import render, get_object_or_404
from .models import Expert


def expert_detail(request, expert_id):
    """
    View that displays the detail page for a specific expert.

    Parameters:
    - expert_id: ID of the Expert to retrieve.

    Logic:
    - Fetches the expert object using the provided ID.
    - Passes the expert instance to the 'experts/expert_detail.html' template.

    Context:
    - expert: The selected Expert instance.

    Returns:
    - Rendered expert detail page.
    """
    expert = get_object_or_404(Expert, id=expert_id)
    return render(request, 'experts/expert_detail.html', {'expert': expert})